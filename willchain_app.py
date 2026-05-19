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
if "grace_period" not in st.session_state:
    st.session_state.grace_period = 90
if "certificate_uploaded" not in st.session_state:
    st.session_state.certificate_uploaded = False
if "certificate_hash" not in st.session_state:
    st.session_state.certificate_hash = None
if "certificate_verified" not in st.session_state:
    st.session_state.certificate_verified = False
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
        "📜 Death Certificate",
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
    total_value = sum(a["value_usd"] for a in st.session_state.assets)

    # Status banner
    if st.session_state.certificate_verified:
        status_html = '<span class="status-danger">🔴 DEATH CERTIFICATE VERIFIED — Transfer executing</span>'
    elif st.session_state.certificate_uploaded:
        status_html = '<span class="status-warning">🟡 CERTIFICATE PENDING VERIFICATION</span>'
    else:
        status_html = '<span class="status-active">🟢 WILL ACTIVE — Waiting for death certificate</span>'

    st.markdown(f"### Will Status &nbsp; {status_html}", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-card">
          <div class="metric-value">{'✅' if st.session_state.certificate_verified else '⏳'}</div>
          <div class="metric-label">Certificate status</div>
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
          <div class="metric-value">{len(st.session_state.assets)}</div>
          <div class="metric-label">Assets registered</div>
        </div>""", unsafe_allow_html=True)

    # How it works box
    st.markdown("#### ⚙️ How WillChain Works")
    st.markdown("""
    <div style="background:white;border-radius:12px;padding:1.5rem;box-shadow:0 2px 12px rgba(0,0,0,0.06)">
      <div style="display:flex;gap:1rem;align-items:flex-start;margin-bottom:1rem">
        <div style="background:#0D1B2A;color:#C9A84C;border-radius:50%;width:32px;height:32px;display:flex;align-items:center;justify-content:center;font-weight:700;flex-shrink:0">1</div>
        <div style="color:#1B2B3E"><strong>Owner registers will on-chain</strong> — wallets, heirs, % allocation stored on Polygon blockchain</div>
      </div>
      <div style="display:flex;gap:1rem;align-items:flex-start;margin-bottom:1rem">
        <div style="background:#0D1B2A;color:#C9A84C;border-radius:50%;width:32px;height:32px;display:flex;align-items:center;justify-content:center;font-weight:700;flex-shrink:0">2</div>
        <div style="color:#1B2B3E"><strong>Upon death</strong> — heir or notary uploads the official death certificate to IPFS</div>
      </div>
      <div style="display:flex;gap:1rem;align-items:flex-start;margin-bottom:1rem">
        <div style="background:#0D1B2A;color:#C9A84C;border-radius:50%;width:32px;height:32px;display:flex;align-items:center;justify-content:center;font-weight:700;flex-shrink:0">3</div>
        <div style="color:#1B2B3E"><strong>Smart contract verifies</strong> the IPFS document hash and authenticity</div>
      </div>
      <div style="display:flex;gap:1rem;align-items:flex-start">
        <div style="background:#3DBE7A;color:white;border-radius:50%;width:32px;height:32px;display:flex;align-items:center;justify-content:center;font-weight:700;flex-shrink:0">✓</div>
        <div style="color:#1B2B3E"><strong>Assets transferred automatically</strong> to heirs' wallets — no bank, no court, no delay</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

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
                          help="Number of days after death certificate submission before transfer executes")
        st.session_state.grace_period = grace

        notif_email = st.text_input("Notification email for heirs", placeholder="heir@example.com")
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

# ── DEATH CERTIFICATE ────────────────────────────────────────────
elif page == "📜 Death Certificate":
    st.markdown("### 📜 Death Certificate — Inheritance Trigger")

    tab_heir, tab_owner = st.tabs(["👤 Heir / Notary View", "ℹ️ How it works"])

    with tab_heir:
        st.info("This page is used by heirs or notaries to trigger the inheritance after the owner's death.")

        if not st.session_state.certificate_verified:
            st.markdown("#### Step 1 — Upload Death Certificate")
            uploaded_file = st.file_uploader(
                "Upload official death certificate (PDF or image)",
                type=["pdf", "png", "jpg", "jpeg"],
                help="The document will be encrypted and stored on IPFS. Only the hash is stored on-chain."
            )

            col1, col2 = st.columns(2)
            with col1:
                notary_name = st.text_input("Notary / Heir full name", placeholder="Me. Jean Dupont")
                notary_role = st.selectbox("Role", ["Notary", "Heir", "Legal Representative", "Estate Lawyer"])
            with col2:
                notary_address = st.text_input("Your wallet address (0x...)", placeholder="0x...")
                death_date = st.date_input("Date of death")

            if uploaded_file and notary_name and notary_address:
                st.markdown("#### Step 2 — Upload to IPFS & Submit to Smart Contract")

                if st.button("📤 Upload to IPFS & Trigger Verification", type="primary", use_container_width=True):
                    with st.status("Processing...", expanded=True) as status:
                        st.write("🔐 Encrypting document...")
                        time.sleep(0.8)
                        ipfs_hash = "QmX" + "".join(random.choices("0123456789abcdefghijklmnopqrstuvwxyz", k=44))
                        st.write(f"📦 Uploading to IPFS... Hash: `{ipfs_hash}`")
                        time.sleep(1)
                        st.write("⛓️ Submitting hash to WillChain smart contract on Polygon...")
                        time.sleep(1)
                        st.write("🔍 Smart contract verifying document authenticity...")
                        time.sleep(1.2)
                        st.session_state.certificate_uploaded = True
                        st.session_state.certificate_hash = ipfs_hash
                        status.update(label="✅ Certificate submitted successfully!", state="complete")

                    st.success(f"✅ Document stored on IPFS and submitted to smart contract!\n\n**IPFS Hash:** `{ipfs_hash}`\n\n**Status:** Pending smart contract verification (simulated: ~30 seconds on testnet)")

                    if st.button("✅ Simulate Smart Contract Verification", type="primary"):
                        with st.spinner("Smart contract verifying..."):
                            time.sleep(2)
                        st.session_state.certificate_verified = True
                        st.rerun()

        else:
            st.success("✅ Death certificate verified by smart contract!")
            st.markdown(f"""
            <div class="contract-box">
            📜 CERTIFICATE VERIFIED<br>
            ─────────────────────────────<br>
            IPFS Hash:   {st.session_state.certificate_hash}<br>
            Status:      ✅ VERIFIED ON-CHAIN<br>
            Trigger:     🔴 INHERITANCE EXECUTING<br>
            Network:     Polygon PoS<br>
            ─────────────────────────────<br>
            Assets transferring to {len(st.session_state.heirs)} heirs...
            </div>
            """, unsafe_allow_html=True)

            total_value = sum(a["value_usd"] for a in st.session_state.assets)
            st.markdown("#### 💸 Transfer Status")
            for h in st.session_state.heirs:
                heir_val = total_value * h["pct"] / 100
                tx = "0x" + "".join(random.choices("0123456789abcdef", k=40))
                st.success(f"✅ **{h['name']}** — ${heir_val:,.0f} sent → `{h['address']}` | Tx: `{tx[:20]}...`")

            if st.button("🔄 Reset Demo"):
                st.session_state.certificate_uploaded = False
                st.session_state.certificate_verified = False
                st.session_state.certificate_hash = None
                st.rerun()

    with tab_owner:
        st.markdown("""
        #### How the death certificate mechanism works

        **For the owner (while alive):**
        - Register your will on-chain once
        - Designate your heirs and asset allocation
        - No monthly action required — ever

        **When the owner passes away:**
        1. An heir or notary obtains the official death certificate
        2. They upload it to this page — document is encrypted and stored on **IPFS**
        3. The IPFS document hash is submitted to the **WillChain smart contract**
        4. The smart contract verifies the document and **automatically transfers all assets** to heirs

        **Why this is better than a monthly ping:**
        - ✅ No burden on the owner while alive
        - ✅ Legally grounded — uses official government documents
        - ✅ Heirs are motivated to act — it's their inheritance
        - ✅ Works anywhere in the world with an official death certificate
        - ✅ Fully decentralized — no company can block the transfer
        """)

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
    st.info("This demo simulates the full inheritance flow — from death certificate upload to automatic asset transfer. Perfect for live presentation.")

    total_value = sum(a["value_usd"] for a in st.session_state.assets)

    st.markdown("#### 📋 Scenario")
    st.markdown("""
    > **Jean Martin** has registered his crypto will on WillChain. He passes away.
    > His daughter **Alice** obtains the official death certificate and triggers the inheritance.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class="metric-card">
          <div class="metric-value">$11,700</div>
          <div class="metric-label">Assets to be transferred</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="metric-card">
          <div class="metric-value">3</div>
          <div class="metric-label">Heirs designated</div>
        </div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("#### 🎬 Run the Demo")

    step = st.radio("Choose step to simulate:", [
        "Step 1 — Heir uploads death certificate to IPFS",
        "Step 2 — Smart contract verifies document",
        "Step 3 — Assets automatically transferred to heirs",
    ])

    if step == "Step 1 — Heir uploads death certificate to IPFS":
        if st.button("▶️ Simulate Step 1", type="primary", use_container_width=True):
            with st.status("Uploading death certificate...", expanded=True) as status:
                st.write("👤 Alice (heir) uploads official death certificate PDF...")
                time.sleep(0.8)
                st.write("🔐 Document encrypted with AES-256...")
                time.sleep(0.8)
                ipfs_hash = "QmX7k9mNpLqR2sT4uV6wX8yZ0aB1cD3eF5gH7iJ9kL2mN4"
                st.write(f"📦 Stored on IPFS: `{ipfs_hash}`")
                time.sleep(0.8)
                st.write("✅ IPFS hash submitted to WillChain smart contract")
                status.update(label="✅ Step 1 complete!", state="complete")
            st.success("Document is now permanently stored on IPFS — censorship resistant, forever accessible.")

    elif step == "Step 2 — Smart contract verifies document":
        if st.button("▶️ Simulate Step 2", type="primary", use_container_width=True):
            with st.status("Smart contract verifying...", expanded=True) as status:
                st.write("⛓️ WillChain contract reads IPFS hash...")
                time.sleep(0.8)
                st.write("🔍 Verifying document structure and authenticity...")
                time.sleep(1)
                st.write("📋 Cross-checking with registered will (owner: Jean Martin)...")
                time.sleep(0.8)
                st.write("✅ Document verified — triggering inheritance mode...")
                status.update(label="✅ Step 2 complete — Inheritance triggered!", state="complete")
            st.success("Smart contract confirmed the death certificate. No human intermediary involved.")

    elif step == "Step 3 — Assets automatically transferred to heirs":
        if st.button("🚀 SIMULATE FULL TRANSFER", type="primary", use_container_width=True):
            with st.status("Executing transfers on Polygon...", expanded=True) as status:
                st.write("💸 AssetTransfer.sol executing...")
                time.sleep(0.8)
                for h in st.session_state.heirs:
                    heir_val = total_value * h["pct"] / 100
                    tx = "0x" + "".join(random.choices("0123456789abcdef", k=40))
                    st.write(f"  ✅ ${heir_val:,.0f} → {h['name']} ({h['address'][:12]}...) | Tx: {tx[:16]}...")
                    time.sleep(0.6)
                st.write("🔒 Will marked as EXECUTED on-chain — immutable.")
                status.update(label="✅ All assets transferred!", state="complete")

            st.success("🎉 Inheritance complete. No bank. No court. No lawyer fees. Pure smart contract.")
            st.balloons()

            st.markdown(f"""
            | Heir | Allocation | Amount Received |
            |---|---|---|
            {''.join(f"| {h['name']} | {h['pct']}% | ${total_value*h['pct']/100:,.0f} |" + chr(10) for h in st.session_state.heirs)}
            """)

# ─── Footer ─────────────────────────────────────────────────────
st.divider()
st.caption("⛓️ WillChain · NEOMA MSc Fintech & DeFi · Final Group Project 2025–2026 · Built with Streamlit + Solidity")
