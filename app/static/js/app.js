/**
 * FraudLens Application Controller
 * Handles live investigation triage, LangGraph step rendering, NetworkX graph, and metrics.
 */

class FraudLensApp {
  constructor() {
    this.transactions = [];
    this.selectedTxnId = null;
    this.currentCase = null;
    this.currentFilter = "ALL";
    this.graphData = null;
    this.nodesWithPos = [];
    this.selectedNode = null;

    this.init();
  }

  async init() {
    this.bindEvents();
    await this.fetchTransactions();
    if (this.transactions.length > 0) {
      this.selectTransaction(this.transactions[0].id);
    }
    this.loadGraphData();
    this.loadMetrics();
  }

  bindEvents() {
    // Navigation Tabs
    document.querySelectorAll(".tab-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const tab = btn.dataset.tab;
        this.switchTab(tab);
      });
    });

    // Risk Filter Pills
    document.querySelectorAll(".filter-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("bg-cyan-600", "text-white"));
        btn.classList.add("bg-cyan-600", "text-white");
        this.currentFilter = btn.dataset.filter;
        this.renderTransactionList();
      });
    });

    // Search Input
    const searchInput = document.getElementById("search-input");
    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        this.renderTransactionList(e.target.value.toLowerCase());
      });
    }

    // Toggle Simulator Panel
    const toggleSimBtn = document.getElementById("toggle-simulator-btn");
    const simPanel = document.getElementById("simulator-panel");
    if (toggleSimBtn && simPanel) {
      toggleSimBtn.addEventListener("click", () => {
        simPanel.classList.toggle("hidden");
        toggleSimBtn.innerText = simPanel.classList.contains("hidden") 
          ? "+ Simulate Custom Transaction" 
          : "− Hide Simulation Form";
      });
    }

    // Custom Simulation Form
    const simForm = document.getElementById("simulation-form");
    if (simForm) {
      simForm.addEventListener("submit", (e) => {
        e.preventDefault();
        this.submitSimulation();
      });
    }

    // Graph Canvas click and hover listeners
    const canvas = document.getElementById("graph-canvas");
    if (canvas) {
      canvas.addEventListener("click", (e) => this.handleCanvasClick(e));
      canvas.addEventListener("mousemove", (e) => this.handleCanvasHover(e));
    }

    // Graph Node Select Dropdown
    const nodeSelect = document.getElementById("graph-node-select");
    if (nodeSelect) {
      nodeSelect.addEventListener("change", (e) => {
        if (e.target.value) {
          this.selectNodeById(e.target.value);
        }
      });
    }
  }

  switchTab(tabName) {
    document.querySelectorAll(".tab-btn").forEach(btn => {
      btn.classList.toggle("active", btn.dataset.tab === tabName);
    });
    document.querySelectorAll(".tab-content").forEach(content => {
      content.classList.toggle("hidden", content.id !== `tab-${tabName}`);
    });

    if (tabName === "graph") {
      setTimeout(() => {
        this.drawGraph();
        if (!this.selectedNode && this.nodesWithPos.length > 0) {
          this.selectNodeById("DEV_BOT_EMU_77");
        }
      }, 50);
    }
  }

  async fetchTransactions() {
    try {
      const res = await fetch("/api/transactions");
      this.transactions = await res.json();
      this.renderTransactionList();
    } catch (err) {
      console.error("Error fetching transactions:", err);
    }
  }

  renderTransactionList(searchQuery = "") {
    const listEl = document.getElementById("transaction-list");
    if (!listEl) return;

    let items = this.transactions;
    if (this.currentFilter !== "ALL") {
      items = items.filter(t => t.severity === this.currentFilter);
    }
    if (searchQuery) {
      items = items.filter(t => 
        t.id.toLowerCase().includes(searchQuery) ||
        t.user_name.toLowerCase().includes(searchQuery) ||
        t.merchant.toLowerCase().includes(searchQuery)
      );
    }

    if (items.length === 0) {
      listEl.innerHTML = `<div class="p-6 text-center text-xs text-slate-500">No matching transactions.</div>`;
      return;
    }

    listEl.innerHTML = items.map(t => {
      const isSelected = t.id === this.selectedTxnId;
      const severity = t.severity || "LOW";
      let badgeClass = "badge-low";
      if (severity === "CRITICAL") badgeClass = "badge-critical";
      else if (severity === "HIGH") badgeClass = "badge-high";
      else if (severity === "MEDIUM") badgeClass = "badge-medium";

      return `
        <div onclick="window.app.selectTransaction('${t.id}')" 
             class="p-3.5 rounded-xl border cursor-pointer transition-all ${
               isSelected 
                 ? 'bg-cyan-950/40 border-cyan-400 shadow-md' 
                 : 'bg-slate-900/60 border-slate-800 hover:border-slate-700 hover:bg-slate-800/40'
             }">
          <div class="flex items-center justify-between">
            <span class="font-mono text-xs font-bold text-slate-200">${t.id}</span>
            <span class="text-[10px] font-semibold px-2 py-0.5 rounded-full ${badgeClass}">
              ${severity} (${t.risk_score})
            </span>
          </div>
          <div class="mt-2 flex justify-between items-baseline">
            <span class="text-sm font-semibold text-white">${t.user_name}</span>
            <span class="font-mono text-sm font-bold text-cyan-400">$${t.amount.toLocaleString(undefined, {minimumFractionDigits: 2})}</span>
          </div>
          <div class="mt-1 flex items-center justify-between text-xs text-slate-400">
            <span class="truncate max-w-[170px]">${t.merchant}</span>
            <span class="text-[11px]">${t.location_city.split(',')[0]}</span>
          </div>
        </div>
      `;
    }).join("");
  }

  async selectTransaction(txnId) {
    this.selectedTxnId = txnId;
    this.renderTransactionList();

    try {
      const res = await fetch(`/api/investigate/${txnId}`);
      this.currentCase = await res.json();
      this.renderCaseWorkspace();
    } catch (err) {
      console.error("Error fetching investigation case:", err);
    }
  }

  renderCaseWorkspace() {
    if (!this.currentCase) return;
    const c = this.currentCase;
    const t = c.transaction;

    // Header Details
    const headerEl = document.getElementById("case-header-details");
    if (headerEl) {
      const score = c.composite_risk_score;
      const severity = c.severity_band;

      let scoreColor = "text-emerald-400";
      let actionBorder = "border-emerald-500/40 bg-emerald-950/30 text-emerald-300";
      if (severity === "CRITICAL") {
        scoreColor = "text-rose-400";
        actionBorder = "border-rose-500/40 bg-rose-950/30 text-rose-300";
      } else if (severity === "HIGH") {
        scoreColor = "text-amber-400";
        actionBorder = "border-amber-500/40 bg-amber-950/30 text-amber-300";
      } else if (severity === "MEDIUM") {
        scoreColor = "text-yellow-400";
        actionBorder = "border-yellow-500/40 bg-yellow-950/30 text-yellow-300";
      }

      headerEl.innerHTML = `
        <div class="space-y-4">
          <!-- Top Row: ID, Score & Action -->
          <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-4">
            <div>
              <span class="text-xs font-mono text-cyan-400 uppercase tracking-widest font-semibold">Active Investigation Case:</span>
              <h2 class="text-lg font-bold text-white font-mono mt-0.5">${c.case_id}</h2>
            </div>
            <div class="flex items-center gap-3">
              <div class="text-right">
                <div class="text-[10px] font-mono text-slate-400 uppercase">Composite Risk Score</div>
                <div class="text-2xl font-black ${scoreColor}">${score} <span class="text-xs text-slate-500">/ 100</span></div>
              </div>
              <span class="text-xs font-bold px-3 py-1.5 rounded-lg uppercase ${severity === 'CRITICAL' ? 'bg-rose-950 text-rose-300 border border-rose-800' : 'bg-slate-800 text-slate-300'}">
                ${severity} RISK
              </span>
            </div>
          </div>

          <!-- Transaction Parameters Grid -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
            <div class="p-3 bg-slate-950/80 rounded-xl border border-slate-800">
              <div class="text-[10px] font-mono text-slate-400 uppercase">Customer</div>
              <div class="font-bold text-white mt-1">${t.user_name}</div>
              <div class="text-[10px] text-slate-500 font-mono">${t.user_id}</div>
            </div>
            <div class="p-3 bg-slate-950/80 rounded-xl border border-slate-800">
              <div class="text-[10px] font-mono text-slate-400 uppercase">Amount</div>
              <div class="font-bold text-cyan-400 mt-1 text-sm">$${t.amount.toLocaleString(undefined, {minimumFractionDigits: 2})}</div>
              <div class="text-[10px] text-slate-500">${t.currency}</div>
            </div>
            <div class="p-3 bg-slate-950/80 rounded-xl border border-slate-800">
              <div class="text-[10px] font-mono text-slate-400 uppercase">Merchant & Category</div>
              <div class="font-bold text-white mt-1 truncate">${t.merchant}</div>
              <div class="text-[10px] text-slate-500 truncate">${t.merchant_category}</div>
            </div>
            <div class="p-3 bg-slate-950/80 rounded-xl border border-slate-800">
              <div class="text-[10px] font-mono text-slate-400 uppercase">Origin Location & IP</div>
              <div class="font-bold text-white mt-1">${t.location_city}</div>
              <div class="text-[10px] text-slate-500 font-mono">${t.ip_address}</div>
            </div>
          </div>

          <!-- Mandated Action Callout -->
          <div class="p-3.5 rounded-xl border ${actionBorder} flex items-center justify-between gap-3">
            <div class="flex items-center gap-2.5">
              <span class="text-lg">🛡️</span>
              <div>
                <div class="text-[10px] font-mono uppercase tracking-wider text-slate-300">Mandated Agentic Safety Action:</div>
                <div class="text-sm font-bold text-white mt-0.5">${c.action_detail}</div>
              </div>
            </div>
            <a href="/api/report/${t.id}/markdown" target="_blank" class="px-3.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-cyan-300 text-xs font-semibold rounded-lg border border-slate-700 transition">
              ⬇ Download Report
            </a>
          </div>

          <!-- Plain-English Executive Summary -->
          <div class="p-4 bg-slate-950/90 rounded-xl border border-slate-800 text-xs text-slate-300 leading-relaxed">
            <span class="font-bold text-cyan-400">Agent Executive Rationale:</span> ${c.executive_summary}
          </div>
        </div>
      `;
    }

    // Multi-Step Reasoning Stepper
    const stepsEl = document.getElementById("reasoning-steps-container");
    if (stepsEl && c.steps_trace) {
      const iconMap = {
        "ML_ANOMALY_DETECTION": "📊",
        "BEHAVIORAL_BASELINE_PROFILING": "👤",
        "DEVICE_AND_GEO_TELEMETRY": "📱",
        "GRAPH_RELATIONSHIP_TRAVERSAL": "🕸️",
        "RAG_PRECEDENT_RETRIEVAL": "📚"
      };

      stepsEl.innerHTML = c.steps_trace.map(s => `
        <div class="step-card p-4 rounded-xl bg-slate-950/80 border border-slate-800">
          <div class="flex items-center justify-between border-b border-slate-800/80 pb-2.5">
            <div class="flex items-center gap-2">
              <span class="text-base">${iconMap[s.node_name] || '⚡'}</span>
              <span class="text-xs font-bold text-white uppercase tracking-wider">Step ${s.step_number}: ${s.node_name.replace(/_/g, ' ')}</span>
            </div>
            <span class="text-[10px] font-mono px-2 py-0.5 bg-slate-900 text-cyan-400 rounded border border-slate-700">${s.tool_name}</span>
          </div>

          <div class="mt-3 text-xs leading-relaxed text-slate-300 bg-slate-900/50 p-2.5 rounded-lg border border-slate-800/60">
            <span class="font-bold text-cyan-300">Agent Cognitive Thought:</span> ${s.thought}
          </div>

          <div class="mt-2.5">
            <div class="text-[11px] font-semibold text-slate-400 mb-1">Evidence Discovered:</div>
            <ul class="space-y-1">
              ${s.findings.map(f => `
                <li class="flex items-start gap-1.5 text-xs text-slate-300">
                  <span class="text-cyan-400">•</span>
                  <span>${f}</span>
                </li>
              `).join('')}
            </ul>
          </div>
        </div>
      `).join("");
    }
  }

  async submitSimulation() {
    const payload = {
      user_id: document.getElementById("sim-user").value,
      amount: parseFloat(document.getElementById("sim-amount").value),
      merchant: document.getElementById("sim-merchant").value,
      merchant_category: document.getElementById("sim-category").value,
      merchant_risk_score: parseFloat(document.getElementById("sim-merchant-risk").value),
      device_id: document.getElementById("sim-device-id").value,
      device_trust_score: parseFloat(document.getElementById("sim-device-trust").value),
      ip_address: document.getElementById("sim-ip").value,
      location_city: document.getElementById("sim-location").value
    };

    try {
      const res = await fetch("/api/simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      await this.fetchTransactions();
      this.selectTransaction(data.transaction.id);

      // Hide simulator
      document.getElementById("simulator-panel").classList.add("hidden");
      document.getElementById("toggle-simulator-btn").innerText = "+ Simulate Custom Transaction";
    } catch (err) {
      console.error("Simulation failed:", err);
    }
  }

  async loadGraphData() {
    try {
      const res = await fetch("/api/graph");
      this.graphData = await res.json();
      this.positionGraphNodes();

      // Populate Node Selector Dropdown
      const selectEl = document.getElementById("graph-node-select");
      if (selectEl && this.graphData.nodes) {
        selectEl.innerHTML = `<option value="">-- Choose Node to Inspect --</option>` +
          this.graphData.nodes.map(n => `<option value="${n.id}">${n.label} (${n.type} - ${n.risk} Risk)</option>`).join("");
      }

      this.drawGraph();

      // Default to inspecting the critical shared emulator
      this.selectNodeById("DEV_BOT_EMU_77");
    } catch (err) {
      console.error("Error loading graph:", err);
    }
  }

  positionGraphNodes() {
    if (!this.graphData) return;
    const canvas = document.getElementById("graph-canvas");
    if (!canvas) return;
    const w = canvas.width;
    const h = canvas.height;

    const clusters = {
      "USER": { x: w * 0.22, y: h * 0.35 },
      "ACCOUNT": { x: w * 0.38, y: h * 0.6 },
      "DEVICE": { x: w * 0.62, y: h * 0.4 },
      "IP": { x: w * 0.78, y: h * 0.65 },
      "MERCHANT": { x: w * 0.5, y: h * 0.82 }
    };

    this.nodesWithPos = this.graphData.nodes.map((n, i) => {
      const c = clusters[n.type] || { x: w / 2, y: h / 2 };
      const angle = (i * 2 * Math.PI) / 8;
      const radius = 45 + ((i % 4) * 20);

      // Distinct placement for the Syndicate Emulator Cluster
      if (n.id === "DEV_BOT_EMU_77" || n.id === "IP_194_26" || n.id === "ACC_88103" || n.id === "ACC_88104" || n.id === "MERCH_MULE_VAULT") {
        return {
          ...n,
          x: w * 0.7 + Math.cos(angle) * 75,
          y: h * 0.32 + Math.sin(angle) * 75,
          radius: 14
        };
      }

      return {
        ...n,
        x: c.x + Math.cos(angle) * radius,
        y: c.y + Math.sin(angle) * radius,
        radius: 12
      };
    });
  }

  selectNodeById(nodeId) {
    if (!this.nodesWithPos || this.nodesWithPos.length === 0) return;
    const node = this.nodesWithPos.find(n => n.id === nodeId);
    if (!node) return;

    this.selectedNode = node;

    // Update select dropdown value if exists
    const selectEl = document.getElementById("graph-node-select");
    if (selectEl && selectEl.value !== nodeId) {
      selectEl.value = nodeId;
    }

    this.drawGraph();
    this.renderNodeInspector(node);
  }

  renderNodeInspector(node) {
    const infoEl = document.getElementById("graph-inspector-info");
    if (!infoEl || !this.graphData) return;

    const connectedEdges = this.graphData.edges.filter(e => e.source === node.id || e.target === node.id);

    let riskBadge = "bg-slate-800 text-slate-300 border border-slate-700";
    if (node.risk === "CRITICAL") riskBadge = "bg-rose-950 text-rose-300 border border-rose-800";
    else if (node.risk === "HIGH") riskBadge = "bg-amber-950 text-amber-300 border border-amber-800";
    else if (node.risk === "LOW") riskBadge = "bg-emerald-950 text-emerald-300 border border-emerald-800";

    infoEl.innerHTML = `
      <div class="space-y-3 text-xs">
        <!-- Node Header -->
        <div class="flex items-center justify-between border-b border-slate-700/80 pb-2.5">
          <div>
            <div class="font-bold text-white text-sm">${node.label}</div>
            <div class="font-mono text-[11px] text-cyan-400 mt-0.5">${node.id}</div>
          </div>
          <div class="text-right">
            <span class="text-[10px] font-mono px-2 py-0.5 rounded font-bold ${riskBadge}">${node.risk} RISK</span>
            <div class="text-[10px] text-slate-400 mt-1 uppercase font-mono">${node.type}</div>
          </div>
        </div>

        <!-- Node description -->
        <div class="p-2.5 bg-slate-900 rounded-lg border border-slate-800 text-slate-300 leading-relaxed">
          ${node.detail || "Active network entity in transaction relationship graph."}
        </div>

        <!-- Connection Summary -->
        <div class="flex justify-between items-center text-[11px] text-slate-400 px-1">
          <span>Connected Entities: <strong class="text-white">${connectedEdges.length}</strong></span>
          <span>Degree Centrality: <strong class="text-white">${node.degree || connectedEdges.length}</strong></span>
        </div>

        <!-- Clickable Connected Links -->
        <div>
          <div class="text-[11px] font-semibold text-slate-400 mb-1.5">Direct Connections (Click to inspect):</div>
          <div class="space-y-1.5 max-h-48 overflow-y-auto pr-1">
            ${connectedEdges.map(e => {
              const otherId = e.source === node.id ? e.target : e.source;
              const otherNode = this.nodesWithPos.find(n => n.id === otherId) || { label: otherId, type: "ENTITY", risk: "LOW" };
              return `
                <button type="button" onclick="window.app.selectNodeById('${otherId}')"
                        class="w-full text-left p-2 bg-slate-900 hover:bg-slate-800 border ${e.alert ? 'border-rose-900/60 hover:border-rose-500' : 'border-slate-800 hover:border-slate-700'} rounded-lg flex items-center justify-between group transition cursor-pointer">
                  <div>
                    <div class="font-semibold text-white group-hover:text-cyan-300 text-xs">${otherNode.label}</div>
                    <div class="text-[10px] text-slate-500 font-mono">${otherId} • ${otherNode.type}</div>
                  </div>
                  <span class="font-mono text-[10px] px-1.5 py-0.5 rounded ${e.alert ? 'bg-rose-950 text-rose-300' : 'bg-slate-800 text-slate-400'}">
                    ${e.relation}
                  </span>
                </button>
              `;
            }).join('')}
          </div>
        </div>
      </div>
    `;
  }

  drawGraph() {
    const canvas = document.getElementById("graph-canvas");
    if (!canvas || !this.nodesWithPos || !this.graphData) return;
    const ctx = canvas.getContext("2d");
    const w = canvas.width;
    const h = canvas.height;

    ctx.clearRect(0, 0, w, h);

    const isNodeSelected = !!this.selectedNode;
    const connectedNodeIds = new Set();
    if (this.selectedNode) {
      connectedNodeIds.add(this.selectedNode.id);
      this.graphData.edges.forEach(e => {
        if (e.source === this.selectedNode.id) connectedNodeIds.add(e.target);
        if (e.target === this.selectedNode.id) connectedNodeIds.add(e.source);
      });
    }

    // 1. Draw Edges
    this.graphData.edges.forEach(e => {
      const src = this.nodesWithPos.find(n => n.id === e.source);
      const tgt = this.nodesWithPos.find(n => n.id === e.target);
      if (!src || !tgt) return;

      const isConnectedToSelected = isNodeSelected && (src.id === this.selectedNode.id || tgt.id === this.selectedNode.id);

      ctx.save();
      if (isNodeSelected && !isConnectedToSelected) {
        ctx.globalAlpha = 0.15;
      }

      ctx.beginPath();
      ctx.moveTo(src.x, src.y);
      ctx.lineTo(tgt.x, tgt.y);

      if (e.alert) {
        ctx.strokeStyle = isConnectedToSelected ? "#f43f5e" : "rgba(244, 63, 94, 0.7)";
        ctx.lineWidth = isConnectedToSelected ? 3.0 : 2.0;
        ctx.setLineDash([4, 3]);
      } else {
        ctx.strokeStyle = isConnectedToSelected ? "#38bdf8" : "#334155";
        ctx.lineWidth = isConnectedToSelected ? 2.5 : 1.2;
        ctx.setLineDash([]);
      }
      ctx.stroke();

      // Draw relation text if connected to selected
      if (isConnectedToSelected) {
        const midX = (src.x + tgt.x) / 2;
        const midY = (src.y + tgt.y) / 2;
        ctx.font = "9px 'JetBrains Mono', monospace";
        ctx.fillStyle = e.alert ? "#fca5a5" : "#7dd3fc";
        ctx.textAlign = "center";
        ctx.fillText(e.relation, midX, midY - 4);
      }

      ctx.restore();
    });

    // 2. Draw Nodes
    this.nodesWithPos.forEach(n => {
      const isSelected = this.selectedNode && this.selectedNode.id === n.id;
      const isNeighbor = this.selectedNode && connectedNodeIds.has(n.id);

      ctx.save();
      if (isNodeSelected && !connectedNodeIds.has(n.id)) {
        ctx.globalAlpha = 0.25;
      }

      let color = "#3b82f6";
      if (n.type === "ACCOUNT") color = "#10b981";
      else if (n.type === "DEVICE") color = "#a855f7";
      else if (n.type === "IP") color = "#f59e0b";
      else if (n.type === "MERCHANT") color = "#06b6d4";

      if (n.risk === "CRITICAL") color = "#f43f5e";

      // Outer Selection Ring
      if (isSelected) {
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.radius + 8, 0, Math.PI * 2);
        ctx.strokeStyle = "#38bdf8";
        ctx.lineWidth = 2.5;
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(n.x, n.y, n.radius + 5, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(56, 189, 248, 0.25)";
        ctx.fill();
      } else if (isNeighbor) {
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.radius + 4, 0, Math.PI * 2);
        ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
        ctx.lineWidth = 1.5;
        ctx.stroke();
      }

      // Main Circle
      ctx.beginPath();
      ctx.arc(n.x, n.y, n.radius, 0, Math.PI * 2);
      ctx.fillStyle = color;
      ctx.fill();
      ctx.strokeStyle = isSelected ? "#ffffff" : "rgba(255, 255, 255, 0.3)";
      ctx.lineWidth = isSelected ? 2.5 : 1;
      ctx.stroke();

      // Label
      ctx.font = isSelected ? "bold 11px Inter, sans-serif" : "10px Inter, sans-serif";
      ctx.fillStyle = isSelected ? "#ffffff" : "#cbd5e1";
      ctx.textAlign = "center";
      ctx.fillText(n.label, n.x, n.y + n.radius + 13);

      ctx.restore();
    });
  }

  handleCanvasClick(e) {
    const canvas = document.getElementById("graph-canvas");
    if (!canvas || !this.nodesWithPos) return;

    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    const x = (e.clientX - rect.left) * scaleX;
    const y = (e.clientY - rect.top) * scaleY;

    // Generous hit-testing radius (+ 12px)
    const clicked = this.nodesWithPos.find(n => {
      const dx = n.x - x;
      const dy = n.y - y;
      return Math.sqrt(dx * dx + dy * dy) <= (n.radius + 12);
    });

    if (clicked) {
      this.selectNodeById(clicked.id);
    }
  }

  handleCanvasHover(e) {
    const canvas = document.getElementById("graph-canvas");
    if (!canvas || !this.nodesWithPos) return;

    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    const x = (e.clientX - rect.left) * scaleX;
    const y = (e.clientY - rect.top) * scaleY;

    const hovered = this.nodesWithPos.find(n => {
      const dx = n.x - x;
      const dy = n.y - y;
      return Math.sqrt(dx * dx + dy * dy) <= (n.radius + 12);
    });

    canvas.style.cursor = hovered ? "pointer" : "default";
  }

  async loadMetrics() {
    try {
      const res = await fetch("/api/metrics");
      const data = await res.json();
      
      const cm = data.confusion_matrix;
      const cmEl = document.getElementById("confusion-matrix-display");
      if (cmEl) {
        cmEl.innerHTML = `
          <div class="grid grid-cols-2 gap-3 text-center text-xs">
            <div class="p-4 bg-emerald-950/40 border border-emerald-500/40 rounded-xl">
              <div class="font-mono text-emerald-400 font-semibold">True Positives (TP)</div>
              <div class="text-2xl font-bold text-white mt-1">${cm.true_positives}</div>
              <div class="text-[10px] text-slate-400 mt-0.5">Fraud correctly captured</div>
            </div>
            <div class="p-4 bg-amber-950/40 border border-amber-500/40 rounded-xl">
              <div class="font-mono text-amber-400 font-semibold">False Positives (FP)</div>
              <div class="text-2xl font-bold text-white mt-1">${cm.false_positives}</div>
              <div class="text-[10px] text-slate-400 mt-0.5">Legitimate transactions flagged</div>
            </div>
            <div class="p-4 bg-rose-950/40 border border-rose-500/40 rounded-xl">
              <div class="font-mono text-rose-400 font-semibold">False Negatives (FN)</div>
              <div class="text-2xl font-bold text-white mt-1">${cm.false_negatives}</div>
              <div class="text-[10px] text-slate-400 mt-0.5">Missed fraud (Minimization goal)</div>
            </div>
            <div class="p-4 bg-slate-900 border border-slate-700 rounded-xl">
              <div class="font-mono text-slate-400 font-semibold">True Negatives (TN)</div>
              <div class="text-2xl font-bold text-white mt-1">${cm.true_negatives}</div>
              <div class="text-[10px] text-slate-400 mt-0.5">Legitimate smoothly approved</div>
            </div>
          </div>
        `;
      }

      const tableEl = document.getElementById("ablation-table");
      if (tableEl && data.comparison) {
        tableEl.innerHTML = data.comparison.map(row => `
          <tr class="border-b border-slate-800 text-xs hover:bg-slate-900/40">
            <td class="py-3 px-4 font-semibold text-white">${row.dimension}</td>
            <td class="py-3 px-4 text-slate-400 font-mono">${row.static_ml}</td>
            <td class="py-3 px-4 text-cyan-400 font-mono font-bold">${row.fraudlens}</td>
            <td class="py-3 px-4 text-emerald-400 font-mono font-semibold">${row.gain}</td>
          </tr>
        `).join("");
      }
    } catch (err) {
      console.error("Error loading metrics:", err);
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  window.app = new FraudLensApp();
});
