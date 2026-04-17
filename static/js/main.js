console.log("Diversity Ventures website loaded.");

/* =========================
   PASSWORD TOGGLE
========================= */
function togglePassword(inputId, button) {
  const input = document.getElementById(inputId);
  if (!input) return;

  if (input.type === "password") {
    input.type = "text";
    button.textContent = "🙈";
  } else {
    input.type = "password";
    button.textContent = "👁";
  }
}

/* =========================
   PASSWORD RULE HELPERS
========================= */
function updateRule(elementId, passed, text) {
  const el = document.getElementById(elementId);
  if (!el) return;

  el.textContent = (passed ? "✓ " : "✗ ") + text;
  el.style.color = passed ? "#4ade80" : "#f87171";
}

function checkPasswordRules(password, prefix, buttonId) {
  const hasLength = password.length >= 8;
  const hasUpper = /[A-Z]/.test(password);
  const hasLower = /[a-z]/.test(password);
  const hasNumber = /[0-9]/.test(password);

  updateRule(`${prefix}rule-length`, hasLength, "At least 8 characters");
  updateRule(`${prefix}rule-upper`, hasUpper, "At least 1 uppercase letter");
  updateRule(`${prefix}rule-lower`, hasLower, "At least 1 lowercase letter");
  updateRule(`${prefix}rule-number`, hasNumber, "At least 1 number");

  const btn = document.getElementById(buttonId);
  if (btn) {
    btn.disabled = !(hasLength && hasUpper && hasLower && hasNumber);
  }
}

/* =========================
   REGISTER PASSWORD CHECK
========================= */
function checkPasswordStrength() {
  const input = document.getElementById("register-password");
  if (!input) return;
  checkPasswordRules(input.value, "", "register-btn");
}

/* =========================
   RESET PASSWORD CHECK
========================= */
function checkResetPasswordStrength() {
  const input = document.getElementById("reset-password");
  if (!input) return;
  checkPasswordRules(input.value, "reset-", "reset-btn");
}

/* =========================
   PROFILE PASSWORD CHECK
========================= */
function checkProfilePasswordStrength() {
  const input = document.getElementById("new-password");
  if (!input) return;
  checkPasswordRules(input.value, "profile-", "profile-save-btn");
}

/* =========================
   WALLET COPY
========================= */
function copyWalletAddress() {
  const walletAddress = document.getElementById("wallet-address");
  const copyMessage = document.getElementById("copy-message");

  if (!walletAddress) return;

  const textToCopy = walletAddress.innerText.trim();

  navigator.clipboard.writeText(textToCopy)
    .then(() => {
      if (copyMessage) {
        copyMessage.innerText = "Copied successfully.";
        setTimeout(() => {
          copyMessage.innerText = "";
        }, 2000);
      }
    })
    .catch(() => {
      if (copyMessage) {
        copyMessage.innerText = "Copy failed.";
      }
    });
}

/* =========================
   PROOF IMAGE PREVIEW
========================= */
function previewProof(event) {
  const file = event.target.files[0];
  const previewBox = document.getElementById("proof-preview-box");
  const previewImage = document.getElementById("proof-preview");

  if (!previewBox || !previewImage) return;

  if (file) {
    const imageUrl = URL.createObjectURL(file);
    previewImage.src = imageUrl;
    previewBox.style.display = "block";
  } else {
    previewBox.style.display = "none";
    previewImage.src = "";
  }
}

/* =========================
   PAYMENT INSTRUCTIONS
========================= */
function updatePaymentInstructions() {
  const paymentMethodSelect = document.getElementById("payment_method");
  const box = document.getElementById("payment-instructions");

  if (!paymentMethodSelect || !box) return;

  const paymentMethod = paymentMethodSelect.value;

  const wallets = {
    USDT: "YOUR_USDT_WALLET_ADDRESS_HERE",
    BTC: "YOUR_BTC_WALLET_ADDRESS_HERE",
    SOL: "YOUR_SOL_WALLET_ADDRESS_HERE",
    USDC: "YOUR_USDC_WALLET_ADDRESS_HERE"
  };

  if (paymentMethod === "Local Currency") {
    box.innerHTML = `
      <h3>Local Currency Instructions</h3>
      <p><strong>Local Currency Selected</strong></p>
      <p>Please contact the official local currency agent on Telegram before completing your payment.</p>
      <div class="wallet-box">
        <div class="wallet-label">Telegram Agent</div>
        <div class="wallet-address" id="wallet-address">@agent_rogermanuel</div>
        <button type="button" class="copy-btn" onclick="copyWalletAddress()">Copy Agent</button>
        <div id="copy-message" class="copy-message"></div>
      </div>
      <p><strong>Note:</strong> After payment, upload your proof and submit for admin review.</p>
    `;
  } else {
    box.innerHTML = `
      <h3>Crypto Payment Instructions</h3>
      <p><strong>${paymentMethod} Payment Selected</strong></p>
      <p>Send your payment to the wallet below, then upload proof and enter your transaction reference.</p>
      <div class="wallet-box">
        <div class="wallet-label">${paymentMethod} Wallet Address</div>
        <div class="wallet-address" id="wallet-address">${wallets[paymentMethod]}</div>
        <button type="button" class="copy-btn" onclick="copyWalletAddress()">Copy Address</button>
        <div id="copy-message" class="copy-message"></div>
      </div>
      <p><strong>Status:</strong> Awaiting admin confirmation after submission.</p>
    `;
  }
}

/* =========================
   AUTO INIT
========================= */
document.addEventListener("DOMContentLoaded", function () {
  if (document.getElementById("payment_method")) {
    updatePaymentInstructions();
  }
});