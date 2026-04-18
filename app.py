from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import random
import re
import requests as req

app = Flask(__name__)
app.secret_key = "diversity_secret_key_change_this"

# =========================
# DATABASE / UPLOAD CONFIG
# =========================
import os
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///database.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "static/uploads"

# =========================
# EMAIL CONFIGURATION
# =========================
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "m73027222@gmail.com"
app.config["MAIL_PASSWORD"] = "grcefjpkobrgmjsm"
app.config["MAIL_DEFAULT_SENDER"] = "m73027222@gmail.com"

# PUBLIC LOGO URL FOR EMAILS
LOGO_URL = "https://yourdomain.com/static/images/logo.png"

db = SQLAlchemy(app)
mail = Mail(app)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# =========================
# LANGUAGE SYSTEM
# =========================
translations = {
    "en": {
        "home": "Home",
        "dashboard": "Dashboard",
        "portal": "Portal",
        "profile": "Profile",
        "login": "Login",
        "register": "Register",
        "logout": "Logout",
        "community": "Community",
        "free_signals": "Free Signals",
        "vip_futures": "VIP Futures",
        "contact": "Contact",
        "welcome": "Welcome",
        "investor_dashboard": "Investor Dashboard",
        "manage_account": "Manage Your Account",
        "hero_title": "Diversity Ventures",
        "hero_subtitle": "Professional onboarding, VIP futures access, free signals, client portal, and a premium community experience for serious traders and investors.",
        "explore_vip": "Explore VIP Futures",
        "free_signals_btn": "Free Signals",
        "register_title": "Create Your Account",
        "register_subtitle": "Join Diversity Ventures and access the client portal.",
        "full_name": "Full Name",
        "email_address": "Email Address",
        "password": "Password",
        "create_account": "Create Account",
        "login_title": "Welcome Back",
        "login_subtitle": "Login to access your client dashboard.",
        "forgot_password": "Forgot Password?",
        "verify_title": "Verify Your Email",
        "verify_subtitle": "Enter the 6-digit code sent to your email.",
        "verify_email": "Verify Email",
        "resend_code": "Resend code",
        "forgot_title": "Forgot Password",
        "forgot_subtitle": "Enter your email to receive a reset code.",
        "send_reset_code": "Send Reset Code",
        "reset_title": "Create a New Password",
        "reset_subtitle": "Enter the code sent to your email and choose a new strong password.",
        "reset_password": "Reset Password",
        "new_password": "New Password",
        "confirm_password": "Confirm New Password",
        "current_password": "Current Password",
        "reset_code": "Reset Code",
        "portal_title": "Submit Your Plan",
        "portal_subtitle": "Select your package, choose a payment method, upload your payment proof, and send your submission for admin review.",
        "package": "Package",
        "payment_method": "Payment Method",
        "transaction_ref": "Transaction Reference / Payment Code",
        "upload_proof": "Upload Payment Proof",
        "notes": "Notes",
        "submit_review": "Submit for Review",
        "dashboard_title": "Investor Dashboard",
        "dashboard_subtitle": "Track your submissions, review status updates, and monitor admin notes in one place.",
        "client": "Client",
        "submissions": "Submissions",
        "account_status": "Account Status",
        "verified_access": "Verified Access",
        "new_submission": "New Submission",
        "your_submissions": "Your Investment & Access Submissions",
        "admin_update": "Admin Update",
        "payment_proof": "Payment Proof",
        "no_submissions": "No submissions yet",
        "open_client_portal": "Open Client Portal",
        "profile_title": "Manage Your Account",
        "profile_subtitle": "Update your personal details and change your password securely.",
        "change_password": "Change Password",
        "save_changes": "Save Changes",
        "vip_title": "Premium Futures Trading Access",
        "vip_subtitle": "Access our VIP futures environment with structured market analysis, premium USDT-pair signals, and disciplined trading support.",
        "signals_daily": "3-9 Signals Daily",
        "signals_daily_text": "Receive carefully selected futures setups shared with a structured trading approach.",
        "usdt_focus": "USDT Pairs Focus",
        "usdt_focus_text": "Focused market attention on actively traded futures pairs for clean execution flow.",
        "vip_subscription": "VIP Subscription",
        "vip_subscription_text": "$100 per month or $250 for 3 months for premium access and continuity.",
        "free_signals_title": "Free Futures Signals & Market Insights",
        "free_signals_subtitle": "Join our public Telegram community to access free futures ideas, selected signals, and daily market insights.",
        "join_telegram": "Join Telegram Community",
        "free_daily_ideas": "Free Daily Ideas",
        "free_daily_ideas_text": "Get selected market opportunities and futures trading perspectives shared publicly.",
        "community_access": "Community Access",
        "community_access_text": "Connect with traders and investors through the official Diversity Ventures Telegram channel.",
        "community_title": "Diversity Ventures Community",
        "community_subtitle": "Our Telegram community is built for investors and traders who want market insights, community support, and interaction around futures trading.",
        "network_title": "Investor & Trader Network",
        "network_text": "Engage with other participants, follow updates, and stay connected to the platform ecosystem.",
        "official_telegram": "Official Telegram",
        "contact_title": "Contact Diversity Ventures",
        "contact_subtitle": "Reach out for support, onboarding guidance, VIP access questions, or community assistance.",
        "contact_channels": "Contact Channels",
        "local_currency_help": "Local Currency Assistance",
        "support_email": "Support Email",
        "email_verification": "Email Verification",
        "password_recovery": "Password Recovery",
        "plan": "Plan",
        "reference": "Reference",
        "no_notes_provided": "No notes provided",
        "no_admin_note": "No admin note yet.",
        "pending_review": "Pending Review",
        "approved": "Approved",
        "rejected": "Rejected",
    },
    "pt": {
        "home": "Inicio",
        "dashboard": "Painel",
        "portal": "Portal",
        "profile": "Perfil",
        "login": "Entrar",
        "register": "Registrar",
        "logout": "Sair",
        "community": "Comunidade",
        "free_signals": "Sinais Gratuitos",
        "vip_futures": "VIP Futures",
        "contact": "Contato",
        "welcome": "Bem-vindo",
        "investor_dashboard": "Painel do Investidor",
        "manage_account": "Gerir Conta",
        "hero_title": "Diversity Ventures",
        "hero_subtitle": "Onboarding profissional, acesso VIP futures, sinais gratuitos, portal do cliente e uma experiencia premium para traders e investidores serios.",
        "explore_vip": "Explorar VIP Futures",
        "free_signals_btn": "Sinais Gratuitos",
        "register_title": "Criar Sua Conta",
        "register_subtitle": "Junte-se a Diversity Ventures e aceda ao portal do cliente.",
        "full_name": "Nome Completo",
        "email_address": "Endereco de Email",
        "password": "Palavra-passe",
        "create_account": "Criar Conta",
        "login_title": "Bem-vindo de Volta",
        "login_subtitle": "Entre para aceder ao seu painel do cliente.",
        "forgot_password": "Esqueceu a palavra-passe?",
        "verify_title": "Verifique o Seu Email",
        "verify_subtitle": "Introduza o codigo de 6 digitos enviado para o seu email.",
        "verify_email": "Verificar Email",
        "resend_code": "Reenviar codigo",
        "forgot_title": "Esqueceu a Palavra-passe",
        "forgot_subtitle": "Introduza o seu email para receber um codigo de redefinicao.",
        "send_reset_code": "Enviar Codigo de Redefinicao",
        "reset_title": "Criar Nova Palavra-passe",
        "reset_subtitle": "Introduza o codigo enviado para o seu email e escolha uma nova palavra-passe forte.",
        "reset_password": "Redefinir Palavra-passe",
        "new_password": "Nova Palavra-passe",
        "confirm_password": "Confirmar Nova Palavra-passe",
        "current_password": "Palavra-passe Atual",
        "reset_code": "Codigo de Redefinicao",
        "portal_title": "Submeta o Seu Plano",
        "portal_subtitle": "Selecione o seu pacote, escolha o metodo de pagamento, carregue a prova de pagamento e envie para revisao do administrador.",
        "package": "Pacote",
        "payment_method": "Metodo de Pagamento",
        "transaction_ref": "Referencia da Transacao / Codigo de Pagamento",
        "upload_proof": "Carregar Prova de Pagamento",
        "notes": "Notas",
        "submit_review": "Enviar para Revisao",
        "dashboard_title": "Painel do Investidor",
        "dashboard_subtitle": "Acompanhe as suas submissoes, reveja atualizacoes de estado e monitorize notas do administrador num so lugar.",
        "client": "Cliente",
        "submissions": "Submissoes",
        "account_status": "Estado da Conta",
        "verified_access": "Acesso Verificado",
        "new_submission": "Nova Submissao",
        "your_submissions": "Os Seus Envios de Investimento e Acesso",
        "admin_update": "Atualizacao do Admin",
        "payment_proof": "Prova de Pagamento",
        "no_submissions": "Ainda nao existem submissoes",
        "open_client_portal": "Abrir Portal do Cliente",
        "profile_title": "Gerir a Sua Conta",
        "profile_subtitle": "Atualize os seus dados pessoais e altere a sua palavra-passe com seguranca.",
        "change_password": "Alterar Palavra-passe",
        "save_changes": "Guardar Alteracoes",
        "vip_title": "Acesso Premium a Futures",
        "vip_subtitle": "Aceda ao nosso ambiente VIP futures com analise estruturada do mercado, sinais premium de pares USDT e suporte disciplinado.",
        "signals_daily": "3-9 Sinais Diarios",
        "signals_daily_text": "Receba setups de futures cuidadosamente selecionados com uma abordagem estruturada.",
        "usdt_focus": "Foco em Pares USDT",
        "usdt_focus_text": "Atencao de mercado focada em pares futures ativos para uma execucao mais limpa.",
        "vip_subscription": "Subscricao VIP",
        "vip_subscription_text": "$100 por mes ou $250 por 3 meses para acesso premium e continuidade.",
        "free_signals_title": "Sinais Gratuitos de Futures e Insights de Mercado",
        "free_signals_subtitle": "Junte-se a nossa comunidade publica no Telegram para aceder a ideias de futures, sinais selecionados e insights diarios de mercado.",
        "join_telegram": "Entrar na Comunidade Telegram",
        "free_daily_ideas": "Ideias Diarias Gratuitas",
        "free_daily_ideas_text": "Receba oportunidades de mercado selecionadas e perspetivas de trading futures partilhadas publicamente.",
        "community_access": "Acesso a Comunidade",
        "community_access_text": "Ligue-se a traders e investidores atraves do canal oficial da Diversity Ventures no Telegram.",
        "community_title": "Comunidade Diversity Ventures",
        "community_subtitle": "A nossa comunidade Telegram foi criada para investidores e traders que procuram insights de mercado, apoio da comunidade e interacao em torno do trading futures.",
        "network_title": "Rede de Investidores e Traders",
        "network_text": "Interaja com outros participantes, acompanhe atualizacoes e mantenha-se ligado ao ecossistema da plataforma.",
        "official_telegram": "Telegram Oficial",
        "contact_title": "Contactar Diversity Ventures",
        "contact_subtitle": "Entre em contacto para suporte, orientacao de onboarding, duvidas sobre VIP ou assistencia da comunidade.",
        "contact_channels": "Canais de Contacto",
        "local_currency_help": "Assistencia em Moeda Local",
        "support_email": "Email de Suporte",
        "email_verification": "Verificacao de Email",
        "password_recovery": "Recuperacao de Palavra-passe",
        "plan": "Plano",
        "reference": "Referencia",
        "no_notes_provided": "Nenhuma nota fornecida",
        "no_admin_note": "Ainda nao existe nota do administrador.",
        "pending_review": "Revisao Pendente",
        "approved": "Aprovado",
        "rejected": "Rejeitado",
    },
    "de": {
        "home": "Startseite",
        "dashboard": "Dashboard",
        "portal": "Portal",
        "profile": "Profil",
        "login": "Anmelden",
        "register": "Registrieren",
        "logout": "Abmelden",
        "community": "Community",
        "free_signals": "Kostenlose Signale",
        "vip_futures": "VIP Futures",
        "contact": "Kontakt",
        "welcome": "Willkommen",
        "investor_dashboard": "Investor Dashboard",
        "manage_account": "Konto verwalten",
        "hero_title": "Diversity Ventures",
        "hero_subtitle": "Professionelles Onboarding, VIP-Futures-Zugang, kostenlose Signale, Kundenportal und ein Premium-Erlebnis fur ernsthafte Trader und Investoren.",
        "explore_vip": "VIP Futures entdecken",
        "free_signals_btn": "Kostenlose Signale",
        "register_title": "Konto erstellen",
        "register_subtitle": "Treten Sie Diversity Ventures bei und erhalten Sie Zugang zum Kundenportal.",
        "full_name": "Vollstandiger Name",
        "email_address": "E-Mail-Adresse",
        "password": "Passwort",
        "create_account": "Konto erstellen",
        "login_title": "Willkommen zuruck",
        "login_subtitle": "Melden Sie sich an, um auf Ihr Kunden-Dashboard zuzugreifen.",
        "forgot_password": "Passwort vergessen?",
        "verify_title": "E-Mail bestatigen",
        "verify_subtitle": "Geben Sie den 6-stelligen Code ein, der an Ihre E-Mail gesendet wurde.",
        "verify_email": "E-Mail bestatigen",
        "resend_code": "Code erneut senden",
        "forgot_title": "Passwort vergessen",
        "forgot_subtitle": "Geben Sie Ihre E-Mail-Adresse ein, um einen Rucksetzcode zu erhalten.",
        "send_reset_code": "Rucksetzcode senden",
        "reset_title": "Neues Passwort erstellen",
        "reset_subtitle": "Geben Sie den an Ihre E-Mail gesendeten Code ein und wahlen Sie ein neues starkes Passwort.",
        "reset_password": "Passwort zurucksetzen",
        "new_password": "Neues Passwort",
        "confirm_password": "Neues Passwort bestatigen",
        "current_password": "Aktuelles Passwort",
        "reset_code": "Rucksetzcode",
        "portal_title": "Plan einreichen",
        "portal_subtitle": "Wahlen Sie Ihr Paket, Ihre Zahlungsmethode, laden Sie Ihren Zahlungsnachweis hoch und senden Sie alles zur Admin-Prufung.",
        "package": "Paket",
        "payment_method": "Zahlungsmethode",
        "transaction_ref": "Transaktionsreferenz / Zahlungscode",
        "upload_proof": "Zahlungsnachweis hochladen",
        "notes": "Notizen",
        "submit_review": "Zur Prufung senden",
        "dashboard_title": "Investor Dashboard",
        "dashboard_subtitle": "Verfolgen Sie Ihre Einreichungen, prufen Sie Statusaktualisierungen und sehen Sie Admin-Notizen an einem Ort.",
        "client": "Kunde",
        "submissions": "Einreichungen",
        "account_status": "Kontostatus",
        "verified_access": "Verifizierter Zugang",
        "new_submission": "Neue Einreichung",
        "your_submissions": "Ihre Investitions- und Zugangs-Einreichungen",
        "admin_update": "Admin-Update",
        "payment_proof": "Zahlungsnachweis",
        "no_submissions": "Noch keine Einreichungen",
        "open_client_portal": "Kundenportal offnen",
        "profile_title": "Konto verwalten",
        "profile_subtitle": "Aktualisieren Sie Ihre personlichen Daten und andern Sie Ihr Passwort sicher.",
        "change_password": "Passwort andern",
        "save_changes": "Anderungen speichern",
        "vip_title": "Premium Futures Zugang",
        "vip_subtitle": "Erhalten Sie Zugang zu unserer VIP-Futures-Umgebung mit strukturierter Marktanalyse, Premium-USDT-Paar-Signalen und disziplinierter Unterstutzung.",
        "signals_daily": "3-9 Signale taglich",
        "signals_daily_text": "Erhalten Sie sorgfaltig ausgewahlte Futures-Setups mit einem strukturierten Ansatz.",
        "usdt_focus": "USDT-Paare Fokus",
        "usdt_focus_text": "Marktfokus auf aktiv gehandelte Futures-Paare fur saubere Ausfuhrung.",
        "vip_subscription": "VIP-Abonnement",
        "vip_subscription_text": "$100 pro Monat oder $250 fur 3 Monate fur Premium-Zugang und Kontinuitat.",
        "free_signals_title": "Kostenlose Futures-Signale & Markt-Insights",
        "free_signals_subtitle": "Treten Sie unserer offentlichen Telegram-Community bei, um kostenlose Futures-Ideen, ausgewahlte Signale und tagliche Markt-Insights zu erhalten.",
        "join_telegram": "Telegram-Community beitreten",
        "free_daily_ideas": "Kostenlose tagliche Ideen",
        "free_daily_ideas_text": "Erhalten Sie ausgewahlte Marktchancen und Futures-Trading-Perspektiven.",
        "community_access": "Community-Zugang",
        "community_access_text": "Verbinden Sie sich mit Tradern und Investoren uber den offiziellen Telegram-Kanal von Diversity Ventures.",
        "community_title": "Diversity Ventures Community",
        "community_subtitle": "Unsere Telegram-Community ist fur Investoren und Trader gedacht, die Marktinformationen, Community-Support und Austausch rund um Futures-Trading suchen.",
        "network_title": "Investoren- & Trader-Netzwerk",
        "network_text": "Treten Sie mit anderen Teilnehmern in Kontakt, verfolgen Sie Updates und bleiben Sie mit dem Plattform-Okosystem verbunden.",
        "official_telegram": "Offizielles Telegram",
        "contact_title": "Diversity Ventures kontaktieren",
        "contact_subtitle": "Kontaktieren Sie uns fur Support, Onboarding-Hilfe, VIP-Fragen oder Community-Unterstutzung.",
        "contact_channels": "Kontaktkanale",
        "local_currency_help": "Lokale Wahrungshilfe",
        "support_email": "Support-E-Mail",
        "email_verification": "E-Mail-Bestatigung",
        "password_recovery": "Passwort-Wiederherstellung",
        "plan": "Plan",
        "reference": "Referenz",
        "no_notes_provided": "Keine Notizen angegeben",
        "no_admin_note": "Noch keine Admin-Notiz.",
        "pending_review": "Ausstehende Prufung",
        "approved": "Genehmigt",
        "rejected": "Abgelehnt",
    }
}


def get_lang():
    return session.get("lang", "en")


def t(key):
    lang = get_lang()
    return translations.get(lang, translations["en"]).get(key, key)


@app.context_processor
def inject_translations():
    return dict(t=t, current_lang=get_lang())


# =========================
# MODELS
# =========================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(10), nullable=True)
    reset_code = db.Column(db.String(10), nullable=True)


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    plan_name = db.Column(db.String(120), nullable=False)
    payment_method = db.Column(db.String(120), nullable=False)
    transaction_ref = db.Column(db.String(200), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    proof_filename = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), default="Pending Review")
    admin_note = db.Column(db.Text, nullable=True)


# =========================
# HELPERS
# =========================
def send_email_code(to_email, subject, plain_body, html_body=None):
    msg = Message(subject, recipients=[to_email])
    msg.body = plain_body
    if html_body:
        msg.html = html_body
    mail.send(msg)


def generate_code():
    return str(random.randint(100000, 999999))


def password_is_strong(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    return True


def build_verification_email_html(full_name, verification_code):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Diversity Ventures Verification</title>
    </head>
    <body style="margin:0;padding:0;background-color:#0b1220;font-family:Arial,Helvetica,sans-serif;color:#ffffff;">
      <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color:#0b1220;padding:30px 0;">
        <tr>
          <td align="center">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0"
              style="max-width:600px;background:#111827;border-radius:18px;overflow:hidden;border:1px solid rgba(255,255,255,0.08);">
              <tr>
                <td align="center" style="padding:28px 24px 18px 24px;background:linear-gradient(135deg,#111827 0%,#0f172a 100%);">
                  <img src="{LOGO_URL}" alt="Diversity Ventures" style="max-width:72px;height:auto;display:block;margin:0 auto 14px auto;">
                  <div style="font-size:22px;font-weight:700;color:#f5c14b;letter-spacing:0.6px;">DIVERSITY VENTURES</div>
                  <div style="margin-top:8px;font-size:13px;color:#94a3b8;">Secure Account Verification</div>
                </td>
              </tr>
              <tr>
                <td style="padding:32px 30px;">
                  <div style="font-size:24px;font-weight:700;color:#ffffff;margin-bottom:14px;">Welcome to Diversity Ventures</div>
                  <div style="font-size:15px;line-height:1.8;color:#cbd5e1;margin-bottom:24px;">
                    Hello {full_name},<br><br>
                    Thank you for creating your account with <strong>Diversity Ventures</strong>.<br>
                    Please use the verification code below to activate your account.
                  </div>
                  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="margin:24px 0;">
                    <tr>
                      <td align="center">
                        <div style="display:inline-block;padding:18px 28px;background:#0f172a;border:1px solid rgba(245,193,75,0.28);border-radius:14px;font-size:34px;letter-spacing:8px;font-weight:700;color:#f5c14b;">
                          {verification_code}
                        </div>
                      </td>
                    </tr>
                  </table>
                  <div style="font-size:14px;line-height:1.8;color:#cbd5e1;margin-top:22px;">
                    For your security, <strong>do not share this code with anyone</strong>.<br>
                    Diversity Ventures will never ask you to disclose your verification code.
                  </div>
                  <div style="margin-top:24px;padding:16px 18px;background:rgba(245,193,75,0.08);border:1px solid rgba(245,193,75,0.16);border-radius:12px;font-size:13px;color:#e2e8f0;line-height:1.7;">
                    If you did not request this email, you can safely ignore it.
                  </div>
                </td>
              </tr>
              <tr>
                <td style="padding:18px 24px;border-top:1px solid rgba(255,255,255,0.06);text-align:center;font-size:12px;color:#94a3b8;">
                  &copy; 2026 Diversity Ventures. All rights reserved.
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """


def build_verification_email_text(full_name, verification_code):
    return f"""Welcome to Diversity Ventures

Hello {full_name},

Thank you for creating your account.

Your verification code is: {verification_code}

Do not share this code with anyone.

If you did not request this email, you can safely ignore it.

Diversity Ventures
"""


def build_reset_email_html(full_name, reset_code):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Diversity Ventures Password Reset</title>
    </head>
    <body style="margin:0;padding:0;background-color:#0b1220;font-family:Arial,Helvetica,sans-serif;color:#ffffff;">
      <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color:#0b1220;padding:30px 0;">
        <tr>
          <td align="center">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0"
              style="max-width:600px;background:#111827;border-radius:18px;overflow:hidden;border:1px solid rgba(255,255,255,0.08);">
              <tr>
                <td align="center" style="padding:28px 24px 18px 24px;background:linear-gradient(135deg,#111827 0%,#0f172a 100%);">
                  <img src="{LOGO_URL}" alt="Diversity Ventures" style="max-width:72px;height:auto;display:block;margin:0 auto 14px auto;">
                  <div style="font-size:22px;font-weight:700;color:#f5c14b;letter-spacing:0.6px;">DIVERSITY VENTURES</div>
                  <div style="margin-top:8px;font-size:13px;color:#94a3b8;">Secure Password Reset</div>
                </td>
              </tr>
              <tr>
                <td style="padding:32px 30px;">
                  <div style="font-size:24px;font-weight:700;color:#ffffff;margin-bottom:14px;">Password Reset Request</div>
                  <div style="font-size:15px;line-height:1.8;color:#cbd5e1;margin-bottom:24px;">
                    Hello {full_name},<br><br>
                    We received a request to reset your password.<br>
                    Please use the reset code below to continue.
                  </div>
                  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="margin:24px 0;">
                    <tr>
                      <td align="center">
                        <div style="display:inline-block;padding:18px 28px;background:#0f172a;border:1px solid rgba(245,193,75,0.28);border-radius:14px;font-size:34px;letter-spacing:8px;font-weight:700;color:#f5c14b;">
                          {reset_code}
                        </div>
                      </td>
                    </tr>
                  </table>
                  <div style="font-size:14px;line-height:1.8;color:#cbd5e1;margin-top:22px;">
                    For your security, <strong>do not share this code with anyone</strong>.<br>
                    Diversity Ventures will never ask you to reveal your reset code.
                  </div>
                  <div style="margin-top:24px;padding:16px 18px;background:rgba(245,193,75,0.08);border:1px solid rgba(245,193,75,0.16);border-radius:12px;font-size:13px;color:#e2e8f0;line-height:1.7;">
                    If you did not request a password reset, you can safely ignore this email.
                  </div>
                </td>
              </tr>
              <tr>
                <td style="padding:18px 24px;border-top:1px solid rgba(255,255,255,0.06);text-align:center;font-size:12px;color:#94a3b8;">
                  &copy; 2026 Diversity Ventures. All rights reserved.
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """


def build_reset_email_text(full_name, reset_code):
    return f"""Diversity Ventures Password Reset

Hello {full_name},

We received a request to reset your password.

Your password reset code is: {reset_code}

Do not share this code with anyone.

If you did not request this, you can safely ignore this email.

Diversity Ventures
"""


# =========================
# LANGUAGE ROUTE
# =========================
@app.route("/set-language/<lang>")
def set_language(lang):
    if lang in ["en", "pt", "de"]:
        session["lang"] = lang
    return redirect(request.referrer or url_for("home"))


# =========================
# PUBLIC ROUTES
# =========================
@app.route("/")
def home():
    coins = [
        {"symbol": "BTCUSDT", "name": "Bitcoin",  "short": "BTC", "logo": "https://assets.coingecko.com/coins/images/1/small/bitcoin.png"},
        {"symbol": "ETHUSDT", "name": "Ethereum", "short": "ETH", "logo": "https://assets.coingecko.com/coins/images/279/small/ethereum.png"},
        {"symbol": "SOLUSDT", "name": "Solana",   "short": "SOL", "logo": "https://assets.coingecko.com/coins/images/4128/small/solana.png"},
        {"symbol": "BNBUSDT", "name": "BNB",      "short": "BNB", "logo": "https://assets.coingecko.com/coins/images/825/small/bnb-icon2_2x.png"},
        {"symbol": "XRPUSDT", "name": "XRP",      "short": "XRP", "logo": "https://assets.coingecko.com/coins/images/44/small/xrp-symbol-white-128.png"},
        {"symbol": "ADAUSDT", "name": "Cardano",  "short": "ADA", "logo": "https://assets.coingecko.com/coins/images/975/small/cardano.png"},
        {"symbol": "DOGEUSDT","name": "Dogecoin", "short": "DOGE","logo": "https://assets.coingecko.com/coins/images/5/small/dogecoin.png"},
    ]

    market_data = []

    for coin in coins:
        try:
            url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={coin['symbol']}"
            response = req.get(url, timeout=5)
            data = response.json()
            price = float(data["lastPrice"])
            change = float(data["priceChangePercent"])
            volume = float(data["quoteVolume"])

            if volume >= 1_000_000_000:
                volume_str = f"${volume / 1_000_000_000:.2f}B"
            elif volume >= 1_000_000:
                volume_str = f"${volume / 1_000_000:.2f}M"
            else:
                volume_str = f"${volume:,.0f}"

            market_data.append({
                "name": coin["name"],
                "short": coin["short"],
                "pair": f"{coin['short']}/USDT",
                "logo": coin["logo"],
                "price": f"${price:,.4f}" if price < 1 else f"${price:,.2f}",
                "change": f"{change:+.2f}%",
                "volume": volume_str,
                "direction": "up" if change >= 0 else "down"
            })
        except Exception:
            market_data.append({
                "name": coin["name"],
                "short": coin["short"],
                "pair": f"{coin['short']}/USDT",
                "logo": coin["logo"],
                "price": "—",
                "change": "—",
                "volume": "—",
                "direction": "up"
            })

    return render_template("index.html", market_data=market_data)


@app.route("/vip-futures")
def vip_futures():
    return render_template("vip_futures.html")


@app.route("/free-signals")
def free_signals():
    return render_template("free_signals.html")


@app.route("/community")
def community():
    return render_template("community.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/packages")
def packages():
    return render_template("packages.html")


@app.route("/results")
def results():
    return render_template("results.html")


# =========================
# AUTH ROUTES
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form["full_name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exists. Please login instead.")
            return redirect(url_for("register"))

        if not password_is_strong(password):
            flash("Password must be at least 8 characters and include uppercase, lowercase, and a number.")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)
        verification_code = generate_code()

        new_user = User(
            full_name=full_name,
            email=email,
            password=hashed_password,
            is_admin=False,
            is_verified=False,
            verification_code=verification_code
        )
        db.session.add(new_user)
        db.session.commit()

        try:
            plain_body = build_verification_email_text(full_name, verification_code)
            html_body = build_verification_email_html(full_name, verification_code)
            send_email_code(email, "Welcome to Diversity Ventures - Verification Code", plain_body, html_body)
            flash("Account created. A verification code has been sent to your email.")
            return redirect(url_for("verify_email", email=email))
        except Exception as e:
            print("MAIL ERROR:", e)
            flash(f"Email could not be sent. Your verification code is: {verification_code}")
            return redirect(url_for("verify_email", email=email))

    return render_template("register.html")


@app.route("/verify-email", methods=["GET", "POST"])
def verify_email():
    email = request.args.get("email", "").strip().lower()

    if request.method == "POST":
        email = request.form["email"].strip().lower()
        code = request.form["code"].strip()

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("User not found.")
            return redirect(url_for("register"))

        if user.verification_code == code:
            user.is_verified = True
            user.verification_code = None
            db.session.commit()
            flash("Email verified successfully. Please login.")
            return redirect(url_for("login"))

        flash("Invalid verification code.")
        return redirect(url_for("verify_email", email=email))

    return render_template("verify_email.html", email=email)


@app.route("/resend-verification/<email>")
def resend_verification(email):
    email = email.strip().lower()
    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User not found.")
        return redirect(url_for("register"))

    if user.is_verified:
        flash("This email is already verified.")
        return redirect(url_for("login"))

    user.verification_code = generate_code()
    db.session.commit()

    try:
        plain_body = build_verification_email_text(user.full_name, user.verification_code)
        html_body = build_verification_email_html(user.full_name, user.verification_code)
        send_email_code(email, "Diversity Ventures - New Verification Code", plain_body, html_body)
        flash("A new verification code has been sent.")
    except Exception as e:
        print("MAIL ERROR:", e)
        flash(f"Email could not be sent. Your verification code is: {user.verification_code}")

    return redirect(url_for("verify_email", email=email))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            if not user.is_verified:
                flash("Please verify your email first.")
                return redirect(url_for("verify_email", email=user.email))

            session["user_id"] = user.id
            session["user_name"] = user.full_name
            session["user_email"] = user.email
            session["is_admin"] = user.is_admin
            flash("Login successful.")
            return redirect(url_for("dashboard"))

        flash("Invalid email or password.")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        user = User.query.filter_by(email=email).first()

        if user:
            reset_code = generate_code()
            user.reset_code = reset_code
            db.session.commit()

            try:
                plain_body = build_reset_email_text(user.full_name, reset_code)
                html_body = build_reset_email_html(user.full_name, reset_code)
                send_email_code(email, "Diversity Ventures Password Reset Code", plain_body, html_body)
                flash("Reset code sent to your email.")
                return redirect(url_for("reset_password", email=email))
            except Exception as e:
                print("MAIL ERROR:", e)
                flash(f"Could not send reset email. Your reset code is: {reset_code}")
                return redirect(url_for("reset_password", email=email))

        flash("Email not found.")
        return redirect(url_for("forgot_password"))

    return render_template("forgot_password.html")


@app.route("/resend-reset/<email>")
def resend_reset(email):
    email = email.strip().lower()
    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User not found.")
        return redirect(url_for("forgot_password"))

    user.reset_code = generate_code()
    db.session.commit()

    try:
        plain_body = build_reset_email_text(user.full_name, user.reset_code)
        html_body = build_reset_email_html(user.full_name, user.reset_code)
        send_email_code(email, "Diversity Ventures - New Password Reset Code", plain_body, html_body)
        flash("A new reset code has been sent.")
    except Exception as e:
        print("MAIL ERROR:", e)
        flash(f"Could not send reset email. Your reset code is: {user.reset_code}")

    return redirect(url_for("reset_password", email=email))


@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    email = request.args.get("email", "").strip().lower()

    if request.method == "POST":
        email = request.form["email"].strip().lower()
        code = request.form["code"].strip()
        new_password = request.form["new_password"]

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("User not found.")
            return redirect(url_for("forgot_password"))

        if user.reset_code != code:
            flash("Invalid reset code.")
            return redirect(url_for("reset_password", email=email))

        if not password_is_strong(new_password):
            flash("Password must be at least 8 characters and include uppercase, lowercase, and a number.")
            return redirect(url_for("reset_password", email=email))

        user.password = generate_password_hash(new_password)
        user.reset_code = None
        db.session.commit()

        flash("Password reset successful. Please login.")
        return redirect(url_for("login"))

    return render_template("reset_password.html", email=email)


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("home"))


# =========================
# USER ROUTES
# =========================
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please login first.")
        return redirect(url_for("login"))

    submissions = Submission.query.filter_by(user_id=session["user_id"]).all()
    return render_template("dashboard.html", submissions=submissions)


@app.route("/investment-portal")
def investment_portal():
    if "user_id" not in session:
        flash("Please login first.")
        return redirect(url_for("login"))
    submissions = Submission.query.filter_by(
        user_id=session["user_id"], status="Approved"
    ).all()
    all_submissions = Submission.query.filter_by(user_id=session["user_id"]).all()
    return render_template("investment_portal.html", submissions=submissions, all_submissions=all_submissions)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        flash("Please login first.")
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    if request.method == "POST":
        full_name = request.form["full_name"].strip()
        email = request.form["email"].strip().lower()
        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if full_name:
            user.full_name = full_name

        if email and email != user.email:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("That email is already in use.")
                return redirect(url_for("profile"))
            user.email = email
            session["user_email"] = email

        if current_password or new_password or confirm_password:
            if not check_password_hash(user.password, current_password):
                flash("Current password is incorrect.")
                return redirect(url_for("profile"))

            if new_password != confirm_password:
                flash("New passwords do not match.")
                return redirect(url_for("profile"))

            if not password_is_strong(new_password):
                flash("New password must be at least 8 characters and include uppercase, lowercase, and a number.")
                return redirect(url_for("profile"))

            user.password = generate_password_hash(new_password)

        db.session.commit()
        session["user_name"] = user.full_name
        flash("Profile updated successfully.")
        return redirect(url_for("profile"))

    return render_template("profile.html", user=user)


@app.route("/portal", methods=["GET", "POST"])
def portal():
    if "user_id" not in session:
        flash("Please login first.")
        return redirect(url_for("login"))

    if request.method == "POST":
        plan_name = request.form["plan_name"]
        payment_method = request.form["payment_method"]
        transaction_ref = request.form["transaction_ref"]
        notes = request.form["notes"]

        proof = request.files.get("proof_file")
        proof_filename = None

        if proof and proof.filename:
            proof_filename = secure_filename(proof.filename)
            proof_path = os.path.join(app.config["UPLOAD_FOLDER"], proof_filename)
            proof.save(proof_path)

        admin_note = "Awaiting admin confirmation."
        if payment_method == "Local Currency":
            admin_note = "Contact local currency agent: @agent_rogermanuel"

        new_submission = Submission(
            user_id=session["user_id"],
            plan_name=plan_name,
            payment_method=payment_method,
            transaction_ref=transaction_ref,
            notes=notes,
            proof_filename=proof_filename,
            status="Pending Review",
            admin_note=admin_note
        )

        db.session.add(new_submission)
        db.session.commit()

        flash("Submission created successfully.")
        return redirect(url_for("dashboard"))

    return render_template("portal.html")


# =========================
# ADMIN ROUTES
# =========================
@app.route("/admin")
def admin():
    if "user_id" not in session or not session.get("is_admin"):
        flash("Access denied.")
        return redirect(url_for("login"))

    submissions = Submission.query.all()
    users = User.query.all()
    user_map = {user.id: user for user in users}

    return render_template("admin.html", submissions=submissions, user_map=user_map)


@app.route("/admin/update/<int:submission_id>", methods=["POST"])
def admin_update(submission_id):
    if "user_id" not in session or not session.get("is_admin"):
        flash("Access denied.")
        return redirect(url_for("login"))

    submission = Submission.query.get_or_404(submission_id)
    submission.status = request.form["status"]
    submission.admin_note = request.form["admin_note"]

    db.session.commit()
    flash("Submission updated successfully.")
    return redirect(url_for("admin"))


# =========================
# RUN APP
# =========================
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)