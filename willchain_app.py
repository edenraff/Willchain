import streamlit as st
import time
from datetime import datetime, timedelta
import random

# ─── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="WillChain",
    page_icon="⛓️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .main { background-color: #F4F6FA; }

  .willchain-hero {
    background: linear-gradient(135deg, #0D1B2A 0%, #1B2B3E 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    color: white;
  }
  .willchain-hero h1 { font-size: 2.4rem; font-weight: 700; margin: 0; }
  .willchain-hero p { color: #C9A84C; font-size: 1.1rem; margin: 0.3rem 0 0; }

  .metric-card {
    background: white;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border-left: 4px solid #C9A84C;
    margin-bottom: 0.8rem;
  }
  .metric-card .metric-value { font-size: 2rem; font-weight: 700; color: #0D1B2A; }
  .metric-card .metric-label { font-size: 0.85rem; color: #888; margin-top: 0.1rem; }

  .status-active {
    background: #ECFDF5;
    border: 1.5px solid #3DBE7A;
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
    color: #047857;
    font-size: 0.82rem;
    font-weight: 600;
    display: inline-block;
  }
  .status-warning {
    background: #FFFBEB;
    border: 1.5px solid #F59E0B;
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
    color: #B45309;
    font-size: 0.82rem;
    font-weight: 600;
    display: inline-block;
  }
  .status-danger {
    background: #FEF2F2;
    border: 1.5px solid #E05252;
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
    color: #B91C1C;
    font-size: 0.82rem;
    font-weight: 600;
    display: inline-block;
  }

  .heir-card {
    background: white;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .ping-btn-area {
    background: linear-gradient(135deg, #0D1B2A, #1B2B3E);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    color: white;
    margin-bottom: 1rem;
  }

  .timeline-step {
    background: white;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.5rem;
    border-left: 3px solid #C9A84C;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  }

  .contract-box {
    background: #0D1B2A;
    border-radius: 12px;
    padding: 1.5rem;
    color: #C9A84C;
    font-family: 'Courier New', monospace;
    font-size: 0.82rem;
    line-height: 1.6;
  }

  div[data-testid="stButton"] button {
    border-radius: 8px;
    font-weight: 600;
  }
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ──────────────────────────────────────────
if "wallet_connected" not in st.session_state:
    st.session_state.wallet_connected = False
if "last_ping" not in st.session_state:
    st.session_state.last_ping = datetime.now() - timedelta(days=12)
if "grace_period" not in st.session_state:
    st.session_state.grace_period = 90
if "heirs" not in st.session_state:
    st.session_state.heirs = [
        {"name": "Alice Dupont", "address": "0xA1b2...C3d4", "pct": 50, "relation": "Spouse"},
        {"name": "Bob Dupont", "address": "0xE5f6...G7h8", "pct": 30, "relation": "Son"},
        {"name": "Claire Dupont", "address": "0xI9j0...K1l2", "pct": 20, "relation": "Daughter"},
    ]
if "assets" not in st.session_state:
    st.session_state.assets = [
        {"token": "ETH", "amount": 2.5, "value_usd": 7500},
        {"token": "MATIC", "amount": 1500, "value_usd": 1200},
        {"token": "USDC", "amount": 3000, "value_usd": 3000},
    ]
if "ping_log" not in st.session_state:
    st.session_state.ping_log = [
        datetime.now() - timedelta(days=d) for d in [12, 42, 73, 105, 135]
    ]
if "will_active" not in st.session_state:
    st.session_state.will_active = True
if "simulation_triggered" not in st.session_state:
    st.session_state.simulation_triggered = False

# ─── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⛓️ WillChain")
    st.caption("Digital Testament on Blockchain")
    st.divider()

    if not st.session_state.wallet_connected:
        st.markdown("### Connect Wallet")
        wallet_choice = st.selectbox("Choose wallet", ["MetaMask", "WalletConnect", "Coinbase Wallet"])
        if st.button("🔗 Connect Wallet", use_container_width=True):
            st.session_state.wallet_connected = True
            st.session_state.wallet_address = "0x742d...35Cc"
            st.rerun()
    else:
        st.success(f"✅ Connected")
        st.code(st.session_state.get("wallet_address", "0x742d...35Cc"))
        st.caption("Network: **Polygon PoS**")
        st.caption("Balance: **2.5 ETH · 1,500 MATIC**")
        if st.button("Disconnect", use_container_width=True):
            st.session_state.wallet_connected = False
            st.rerun()

    st.divider()
    st.markdown("### Navigation")
    page = st.radio("", [
        "🏠 Dashboard",
        "📝 My Will",
        "👥 Heirs",
        "💰 Assets",
        "🔔 Alive Signal",
        "🔬 Smart Contract",
        "🎭 Demo Simulator",
    ], label_visibility="collapsed")

# ─── Main Content ────────────────────────────────────────────────

# Hero
st.markdown("""
<div class="willchain-hero">
  <h1>⛓️ WillChain</h1>
  <p>Your crypto assets, automatically transmitted to your heirs — forever.</p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.wallet_connected:
    st.info("👆 Connect your wallet in the sidebar to get started.")
    st.stop()

# ── DASHBOARD ────────────────────────────────────────────────────
if page == "🏠 Dashboard":
    days_since_ping = (datetime.now() - st.session_state.last_ping).days
    days_remaining = st.session_state.grace_period - days_since_ping
    pct_elapsed = min(days_since_ping / st.session_state.grace_period, 1.0)
    total_value = sum(a["value_usd"] for a in st.session_state.assets)

    # Status banner
    if days_remaining > 30:
        status_html = '<span class="status-active">🟢 WILL ACTIVE — Safe</span>'
    elif days_remaining > 7:
        status_html = '<span class="status-warning">🟡 PING REQUIRED SOON</span>'
    else:
        status_html = '<span class="status-danger">🔴 CRITICAL — Trigger Imminent</span>'

    st.markdown(f"### Will Status &nbsp; {status_html}", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-card">
          <div class="metric-value">{days_remaining}d</div>
          <div class="metric-label">Days until trigger</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card">
          <div class="metric-value">${total_value:,.0f}</div>
          <div class="metric-label">Total assets registered</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card">
          <div class="metric-value">{len(st.session_state.heirs)}</div>
          <div class="metric-label">Designated heirs</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card">
          <div class="metric-value">{days_since_ping}d</div>
          <div class="metric-label">Since last ping</div>
        </div>""", unsafe_allow_html=True)

    # Progress bar
    st.markdown("#### ⏱️ Grace Period Progress")
    progress_color = "normal" if pct_elapsed < 0.7 else ("warning" if pct_elapsed < 0.9 else "error")
    st.progress(pct_elapsed, text=f"{days_since_ping} / {st.session_state.grace_period} days elapsed")

    if days_remaining <= 30:
        st.warning(f"⚠️ **Action required:** You have {days_remaining} days to send your alive signal before inheritance is triggered.")

    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 👥 Heir Allocations")
        for h in st.session_state.heirs:
            heir_value = total_value * h["pct"] / 100
            st.markdown(f"""<div class="heir-card">
              <div style="font-size:1.5rem">👤</div>
              <div style="flex:1">
                <div style="font-weight:600;color:#0D1B2A">{h['name']}</div>
                <div style="font-size:0.8rem;color:#888">{h['relation']} · {h['address']}</div>
              </div>
              <div style="text-align:right">
                <div style="font-weight:700;color:#C9A84C">{h['pct']}%</div>
                <div style="font-size:0.8rem;color:#888">${heir_value:,.0f}</div>
              </div>
            </div>""", unsafe_allow_html=True)

    with col_b:
        st.markdown("#### 💰 Registered Assets")
        for a in st.session_state.assets:
            st.markdown(f"""<div class="heir-card">
              <div style="font-size:1.5rem">🪙</div>
              <div style="flex:1">
                <div style="font-weight:600;color:#0D1B2A">{a['token']}</div>
                <div style="font-size:0.8rem;color:#888">{a['amount']} tokens</div>
              </div>
              <div style="text-align:right">
                <div style="font-weight:700;color:#0D1B2A">${a['value_usd']:,}</div>
              </div>
            </div>""", unsafe_allow_html=True)

# ── MY WILL ──────────────────────────────────────────────────────
elif page == "📝 My Will":
    st.markdown("### 📝 My Will Configuration")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Settings")
        grace = st.slider("Grace period (days)", 30, 365, st.session_state.grace_period,
                          help="Number of days without a ping before inheritance is triggered")
        st.session_state.grace_period = grace

        ping_freq = st.selectbox("Ping reminder frequency", ["Weekly", "Monthly", "Every 2 weeks"])
        notif_email = st.text_input("Notification email", placeholder="you@example.com")
        multisig = st.checkbox("Require multi-heir confirmation (M-of-N)", value=False)
        if multisig:
            m = st.slider("Minimum confirmations required (M)", 1, len(st.session_state.heirs),
                          min(2, len(st.session_state.heirs)))

    with col2:
        st.markdown("#### Will Summary")
        st.markdown(f"""
        <div class="contract-box">
        📋 WILL CONFIGURATION<br>
        ─────────────────────────────<br>
        Owner:        {st.session_state.get('wallet_address', '0x742d...35Cc')}<br>
        Network:      Polygon PoS<br>
        Grace Period: {grace} days<br>
        Heirs:        {len(st.session_state.heirs)}<br>
        Assets:       {len(st.session_state.assets)} tokens<br>
        Total Value:  ${sum(a['value_usd'] for a in st.session_state.assets):,}<br>
        Multi-sig:    {'Enabled' if multisig else 'Disabled'}<br>
        Status:       {'🟢 ACTIVE' if st.session_state.will_active else '🔴 INACTIVE'}<br>
        ─────────────────────────────<br>
        Last Ping:    {st.session_state.last_ping.strftime('%Y-%m-%d %H:%M')}<br>
        IPFS Hash:    QmX7k9...abc123<br>
        Contract:     0x9aB3...Fd2e (Polygon)
        </div>
        """, unsafe_allow_html=True)

        if st.button("💾 Save Configuration to Blockchain", use_container_width=True, type="primary"):
            with st.spinner("Broadcasting transaction to Polygon..."):
                time.sleep(1.5)
            st.success("✅ Configuration saved on-chain! Tx: 0xfa3b...9c12")

# ── HEIRS ────────────────────────────────────────────────────────
elif page == "👥 Heirs":
    st.markdown("### 👥 Heir Management")

    # Display existing heirs
    st.markdown("#### Current Heirs")
    total_pct = sum(h["pct"] for h in st.session_state.heirs)
    total_value = sum(a["value_usd"] for a in st.session_state.assets)

    for i, h in enumerate(st.session_state.heirs):
        with st.expander(f"👤 {h['name']} — {h['pct']}% (${total_value * h['pct'] / 100:,.0f})", expanded=False):
            col1, col2, col3 = st.columns(3)
            with col1: st.text_input("Full Name", h["name"], key=f"hname_{i}")
            with col2: st.text_input("Wallet Address", h["address"], key=f"haddr_{i}")
            with col3: st.text_input("Relation", h["relation"], key=f"hrel_{i}")
            new_pct = st.slider(f"Allocation %", 0, 100, h["pct"], key=f"hpct_{i}")
            if st.button(f"Remove heir", key=f"rem_{i}"):
                st.session_state.heirs.pop(i)
                st.rerun()

    # Allocation chart
    st.markdown("#### Allocation Overview")
    if total_pct != 100:
        st.warning(f"⚠️ Total allocation is {total_pct}% — must equal 100%")
    else:
        st.success("✅ Allocation sums to 100%")

    import json
    labels = [h["name"] for h in st.session_state.heirs]
    values = [h["pct"] for h in st.session_state.heirs]
    st.bar_chart({h["name"]: h["pct"] for h in st.session_state.heirs})

    # Add heir form
    st.markdown("#### ➕ Add New Heir")
    with st.form("add_heir"):
        c1, c2, c3, c4 = st.columns(4)
        new_name = c1.text_input("Full Name")
        new_addr = c2.text_input("Wallet Address (0x...)")
        new_rel = c3.text_input("Relation")
        new_pct_input = c4.number_input("Allocation %", 0, 100, 0)
        submitted = st.form_submit_button("Add Heir", use_container_width=True)
        if submitted and new_name and new_addr:
            st.session_state.heirs.append({
                "name": new_name, "address": new_addr,
                "pct": new_pct_input, "relation": new_rel
            })
            st.success(f"✅ {new_name} added as heir!")
            st.rerun()

# ── ASSETS ───────────────────────────────────────────────────────
elif page == "💰 Assets":
    st.markdown("### 💰 Registered Assets")
    total_value = sum(a["value_usd"] for a in st.session_state.assets)

    st.markdown(f"**Total Portfolio Value: ${total_value:,}**")

    for i, a in enumerate(st.session_state.assets):
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        col1.metric("Token", a["token"])
        col2.metric("Amount", f"{a['amount']:,}")
        col3.metric("Value (USD)", f"${a['value_usd']:,}")
        if col4.button("🗑️", key=f"del_asset_{i}"):
            st.session_state.assets.pop(i)
            st.rerun()

    st.divider()
    st.markdown("#### ➕ Add Asset")
    with st.form("add_asset"):
        c1, c2, c3 = st.columns(3)
        tok = c1.selectbox("Token", ["ETH", "MATIC", "USDC", "USDT", "WBTC", "DAI", "LINK", "Other"])
        amt = c2.number_input("Amount", 0.0, step=0.01)
        val = c3.number_input("Value (USD)", 0.0, step=1.0)
        if st.form_submit_button("Add Asset"):
            st.session_state.assets.append({"token": tok, "amount": amt, "value_usd": val})
            st.success(f"✅ {tok} added!")
            st.rerun()

    st.divider()
    st.markdown("#### 📊 Portfolio Breakdown")
    chart_data = {a["token"]: a["value_usd"] for a in st.session_state.assets}
    st.bar_chart(chart_data)

# ── ALIVE SIGNAL ─────────────────────────────────────────────────
elif page == "🔔 Alive Signal":
    days_since = (datetime.now() - st.session_state.last_ping).days
    days_remaining = st.session_state.grace_period - days_since

    st.markdown("### 🔔 Alive Signal — Dead-Man's Switch")

    st.markdown(f"""
    <div class="ping-btn-area">
      <div style="font-size:3rem;margin-bottom:0.5rem">❤️</div>
      <div style="font-size:1.3rem;font-weight:700;margin-bottom:0.3rem">I am alive.</div>
      <div style="color:#8899AA;margin-bottom:1.5rem">
        Last signal: <strong>{st.session_state.last_ping.strftime('%d %b %Y at %H:%M')}</strong> ({days_since} days ago)<br>
        Next trigger in: <strong style="color:#C9A84C">{days_remaining} days</strong>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅  SEND ALIVE SIGNAL", use_container_width=True, type="primary"):
            with st.spinner("Sending transaction to Polygon blockchain..."):
                time.sleep(2)
            st.session_state.last_ping = datetime.now()
            st.session_state.ping_log.insert(0, datetime.now())
            tx_hash = "0x" + "".join(random.choices("0123456789abcdef", k=40))
            st.success(f"✅ Signal confirmed on-chain!\n\nTx: `{tx_hash}`\nBlock: #{random.randint(40000000, 50000000)}\nGas used: 0.00003 MATIC")
            st.balloons()
            time.sleep(1)
            st.rerun()

    # Ping history
    st.markdown("#### 📅 Ping History")
    for i, ping_date in enumerate(st.session_state.ping_log[:8]):
        days_ago = (datetime.now() - ping_date).days
        label = "Today" if days_ago == 0 else f"{days_ago} days ago"
        st.markdown(f"""<div class="timeline-step">
          {'🟢' if i == 0 else '⚪'} <strong>{ping_date.strftime('%d %B %Y — %H:%M')}</strong>
          &nbsp;&nbsp;<span style="color:#888;font-size:0.85rem">{label}</span>
        </div>""", unsafe_allow_html=True)

# ── SMART CONTRACT ───────────────────────────────────────────────
elif page == "🔬 Smart Contract":
    st.markdown("### 🔬 Smart Contract — Technical View")

    tab1, tab2, tab3 = st.tabs(["DeadManSwitch.sol", "WillRegistry.sol", "AssetTransfer.sol"])

    with tab1:
        st.code("""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title DeadManSwitch
 * @notice Core WillChain contract — triggers inheritance after inactivity
 * @dev Deployed on Polygon PoS for gas efficiency
 */
contract DeadManSwitch is ReentrancyGuard {

    address public owner;
    uint256 public lastPingTimestamp;
    uint256 public gracePeriod;        // in seconds
    bool    public triggered;

    event AlivePing(address indexed owner, uint256 timestamp);
    event InheritanceTriggered(address indexed owner, uint256 timestamp);
    event GracePeriodUpdated(uint256 newPeriod);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    modifier notTriggered() {
        require(!triggered, "Already triggered");
        _;
    }

    constructor(uint256 _gracePeriodDays) {
        owner             = msg.sender;
        lastPingTimestamp = block.timestamp;
        gracePeriod       = _gracePeriodDays * 1 days;
        triggered         = false;
    }

    /**
     * @notice Owner sends alive signal — resets the countdown
     */
    function ping() external onlyOwner notTriggered {
        lastPingTimestamp = block.timestamp;
        emit AlivePing(msg.sender, block.timestamp);
    }

    /**
     * @notice Check if inheritance should be triggered
     * @return bool — true if grace period has elapsed
     */
    function shouldTrigger() public view returns (bool) {
        return block.timestamp >= lastPingTimestamp + gracePeriod;
    }

    /**
     * @notice Anyone can call this after grace period expires
     *         Triggers AssetTransfer contract
     */
    function triggerInheritance() external nonReentrant notTriggered {
        require(shouldTrigger(), "Grace period not elapsed");
        triggered = true;
        emit InheritanceTriggered(owner, block.timestamp);
        // Calls AssetTransfer.executeTransfers()
    }

    /**
     * @notice Owner can update grace period at any time
     */
    function updateGracePeriod(uint256 _days) external onlyOwner notTriggered {
        gracePeriod = _days * 1 days;
        emit GracePeriodUpdated(_days);
    }

    /**
     * @notice Returns days remaining before trigger
     */
    function daysUntilTrigger() external view returns (int256) {
        uint256 triggerTime = lastPingTimestamp + gracePeriod;
        if (block.timestamp >= triggerTime) return 0;
        return int256((triggerTime - block.timestamp) / 1 days);
    }
}""", language="solidity")

    with tab2:
        st.code("""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title WillRegistry
 * @notice Stores heir designations and asset allocations on-chain
 */
contract WillRegistry {

    struct Heir {
        address wallet;
        uint256 percentage;   // in basis points (10000 = 100%)
        string  ipfsMetadata; // Encrypted heir info stored on IPFS
    }

    address public owner;
    Heir[]  public heirs;
    string  public willIpfsHash;  // Encrypted full will on IPFS
    bool    public isActive;

    event HeirAdded(address indexed heir, uint256 percentage);
    event WillUpdated(string ipfsHash);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    constructor() {
        owner    = msg.sender;
        isActive = true;
    }

    function addHeir(
        address _wallet,
        uint256 _percentage,
        string memory _ipfsMetadata
    ) external onlyOwner {
        heirs.push(Heir(_wallet, _percentage, _ipfsMetadata));
        emit HeirAdded(_wallet, _percentage);
    }

    function validateAllocations() public view returns (bool) {
        uint256 total;
        for (uint i = 0; i < heirs.length; i++) {
            total += heirs[i].percentage;
        }
        return total == 10000; // Must sum to 100%
    }

    function getHeirs() external view returns (Heir[] memory) {
        return heirs;
    }

    function updateWillDocument(string memory _ipfsHash) external onlyOwner {
        willIpfsHash = _ipfsHash;
        emit WillUpdated(_ipfsHash);
    }
}""", language="solidity")

    with tab3:
        st.code("""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title AssetTransfer
 * @notice Executes asset distribution to heirs upon inheritance trigger
 */
contract AssetTransfer is ReentrancyGuard {

    address public registry;   // WillRegistry address
    address public switchAddr; // DeadManSwitch address

    event TransferExecuted(address indexed heir, address token, uint256 amount);

    constructor(address _registry, address _switch) {
        registry   = _registry;
        switchAddr = _switch;
    }

    modifier onlySwitch() {
        require(msg.sender == switchAddr, "Only DeadManSwitch");
        _;
    }

    /**
     * @notice Distribute ERC-20 tokens to heirs per allocation
     * @param token  ERC-20 token address
     * @param total  Total amount to distribute
     * @param heirs  Array of heir addresses
     * @param pcts   Array of percentages (basis points)
     */
    function distributeERC20(
        address token,
        uint256 total,
        address[] calldata heirs,
        uint256[] calldata pcts
    ) external onlySwitch nonReentrant {
        require(heirs.length == pcts.length, "Length mismatch");

        IERC20 erc20 = IERC20(token);

        for (uint i = 0; i < heirs.length; i++) {
            uint256 amount = (total * pcts[i]) / 10000;
            require(erc20.transfer(heirs[i], amount), "Transfer failed");
            emit TransferExecuted(heirs[i], token, amount);
        }
    }

    /**
     * @notice Distribute native ETH/MATIC to heirs
     */
    function distributeNative(
        address[] calldata heirs,
        uint256[] calldata pcts
    ) external payable onlySwitch nonReentrant {
        uint256 total = msg.value;
        for (uint i = 0; i < heirs.length; i++) {
            uint256 amount = (total * pcts[i]) / 10000;
            (bool ok, ) = heirs[i].call{value: amount}("");
            require(ok, "ETH transfer failed");
            emit TransferExecuted(heirs[i], address(0), amount);
        }
    }
}""", language="solidity")

    st.divider()
    st.markdown("#### 📋 Deployed Contract Info (Testnet)")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        | Contract | Address |
        |---|---|
        | DeadManSwitch | `0x9aB3...Fd2e` |
        | WillRegistry | `0x1cD4...Ae5f` |
        | AssetTransfer | `0x7bE2...Cc9d` |
        """)
    with col2:
        st.markdown("""
        | Parameter | Value |
        |---|---|
        | Network | Polygon Mumbai (testnet) |
        | Solidity | 0.8.19 |
        | OpenZeppelin | 4.9.3 |
        | Gas / ping tx | ~$0.00003 |
        """)

# ── DEMO SIMULATOR ───────────────────────────────────────────────
elif page == "🎭 Demo Simulator":
    st.markdown("### 🎭 Inheritance Demo Simulator")
    st.info("This demo simulates what happens when the grace period expires and inheritance is triggered. Perfect for live presentation.")

    total_value = sum(a["value_usd"] for a in st.session_state.assets)

    st.markdown("#### Scenario Setup")
    col1, col2 = st.columns(2)
    with col1:
        sim_days = st.slider("Simulate: days without ping", 0, 120, 95)
        sim_grace = st.slider("Grace period set by owner (days)", 30, 120, 90)
    with col2:
        sim_days_remaining = sim_grace - sim_days
        if sim_days_remaining > 0:
            st.success(f"✅ Will is safe — {sim_days_remaining} days remaining")
        else:
            st.error(f"🔴 Grace period expired {abs(sim_days_remaining)} days ago — TRIGGER READY")

    st.divider()

    if sim_days_remaining <= 0:
        st.markdown("#### 🚨 Inheritance Trigger Simulation")
        if st.button("🚀 EXECUTE INHERITANCE TRIGGER", type="primary", use_container_width=True):
            st.session_state.simulation_triggered = True

        if st.session_state.simulation_triggered:
            with st.status("Executing on-chain inheritance...", expanded=True) as status:
                st.write("🔍 Verifying grace period elapsed...")
                time.sleep(0.8)
                st.write("📋 Reading WillRegistry — fetching heir list...")
                time.sleep(0.8)
                st.write("💸 Executing AssetTransfer.distributeNative()...")
                time.sleep(0.8)
                for h in st.session_state.heirs:
                    heir_val = total_value * h["pct"] / 100
                    st.write(f"  ✅ Sent ${heir_val:,.0f} → {h['name']} ({h['address']})")
                    time.sleep(0.5)
                st.write("📝 Recording InheritanceTriggered event on Polygon...")
                time.sleep(0.5)
                st.write("🔒 Will marked as EXECUTED — immutable.")
                status.update(label="✅ Inheritance executed successfully!", state="complete")

            st.success("🎉 All assets transferred automatically. No lawyer. No court. No delay. Pure smart contract.")
            st.markdown(f"""
            | Heir | Allocation | Amount |
            |---|---|---|
            {''.join(f"| {h['name']} | {h['pct']}% | ${total_value*h['pct']/100:,.0f} |" for h in st.session_state.heirs)}
            """)
            if st.button("🔄 Reset Simulation"):
                st.session_state.simulation_triggered = False
                st.rerun()
    else:
        st.markdown("#### 🟢 Will is Active")
        st.markdown(f"Increase the 'days without ping' slider above {sim_grace} to simulate a trigger.")

# ─── Footer ─────────────────────────────────────────────────────
st.divider()
st.caption("⛓️ WillChain · NEOMA MSc Fintech & DeFi · Final Group Project 2025–2026 · Built with Streamlit + Solidity")
