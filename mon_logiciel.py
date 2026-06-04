import streamlit as st
import pandas as pd
import smtplib
import time
import re
from email.message import EmailMessage
import random

st.set_page_config(page_title="ApplyAuto - Assistant de Candidature", layout="wide", page_icon="🚀")

DOMAINES_GENERIQUES = {
    "gmail.com", "yahoo.com", "yahoo.fr", "hotmail.com", "hotmail.fr", 
    "outlook.com", "outlook.fr", "live.com", "live.fr", "orange.fr", 
    "free.fr", "sfr.fr", "laposte.net", "icloud.com", "msn.com", "aol.com", "bbox.fr"
}

def deviner_entreprise_depuis_email(email):
    """Extrait le nom de l'entreprise du domaine s'il n'est pas générique."""
    try:
        domaine = email.split('@')[1].lower()
        if domaine in DOMAINES_GENERIQUES:
            return ""
        
        nom_brut = domaine.split('.')[0]
        nom_propre = nom_brut.replace('-', ' ').title()
        return nom_propre
    except:
        return ""

# --- TEXTES RELIGIEUX ---
verset_fixe = "﴿ وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ ۚ إِنَّ اللَّهَ بَالِغُ أَمْرِهِ ﴾"

invocations = [
    "توكلت على الله ولا حول ولا قوة إلا بالله، توكلت على الله الذي لا يغلبه أحد",
    "توكلت على الجبار الذي لا يقهره أحد، توكلت على العزيز الرحيم",
    "توكلت على الذي يراني وتقلبي في الساجدين، توكلت على الحي الذي لا يموت",
    "يا رب إني توكلت عليك، فإنك كل شيء بيدك، فحقق لنا أحلامنا وأمنياتنا يا رب العالمين",
    "توكلت عليك يا رب العالمين فإنك الأحد الصمد الذي لم يلد ولم يولد، ولم يكن له كفوا أحد",
    "اللهم إني توكلت عليك، فاكتب لي نجاحا في كل أموري، ووفقني في طريقي",
    "يارب كن معي في كل أمر وهيئ لي كا ما أسعى عليه، فإنك قادر على كل شيء"
]
texte_bandeau = " ۞ ".join(invocations) + " ۞ "

# --- CSS POUR LE BANDEAU FIXE (AVEC FOND SOLIDE ADAPTATIF) ---
st.markdown(f"""
    <style>
    .footer-scrolling {{
        position: fixed; 
        bottom: 0; 
        left: 0; 
        width: 100%;
        /* Fond solide qui s'adapte au mode clair ou sombre de l'ordinateur */
        background-color: var(--background-color); 
        border-top: 2px solid var(--secondary-background-color);
        padding: 12px 0;
        z-index: 9999;
    }}
    marquee {{
        font-size: 22px;
        font-family: 'Amiri', 'Arial', sans-serif;
        font-weight: bold;
        color: var(--text-color);
    }}
    .block-container {{ padding-bottom: 90px; }}
    </style>
    <div class="footer-scrolling">
        <marquee direction="right" scrollamount="6">
            {texte_bandeau}
        </marquee>
    </div>
""", unsafe_allow_html=True)

# --- INITIALISATION DE LA MÉMOIRE ---
if 'invocation_lue' not in st.session_state:
    st.session_state.invocation_lue = False

def demarrer_application():
    st.session_state.invocation_lue = True

# ==========================================================
# PAGE 1 : ÉCRAN D'ACCUEIL
# ==========================================================
if not st.session_state.invocation_lue:
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    
    st.markdown(f"<h1 style='text-align: center; direction: rtl; font-family: Amiri, Arial, sans-serif; line-height: 1.8; font-size: 44px;'>{verset_fixe}</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; font-weight: 300; opacity: 0.8;'>✨ Avant de commencer votre recherche de stage, plaçons notre confiance en Dieu ✨</h4>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.button("بِسْمِ اللَّهِ - Commencer l'application", use_container_width=True, on_click=demarrer_application)

# ==========================================================
# PAGE 2 : APPLICATION PRINCIPALE
# ==========================================================
else:
    st.markdown(f"<h3 style='text-align: center; direction: rtl; font-family: Amiri, Arial, sans-serif; color: #1f77b4; padding-bottom: 10px;'>{verset_fixe}</h3>", unsafe_allow_html=True)
    
    st.title("🚀 ApplyAuto : Logiciel d'Envoi de Candidatures")
    st.markdown("Automatisez vos demandes de stage facilement. **Vos identifiants ne sont pas sauvegardés.**")

    def extraire_emails_simples(texte):
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = list(set(re.findall(pattern, str(texte))))
        return [{"email": e, "entreprise": deviner_entreprise_depuis_email(e), "contact": ""} for e in emails]

    with st.sidebar:
        st.header("🔑 Connexion Gmail")
        st.markdown("""
        *Pour des raisons de sécurité, Google demande un mot de passe d'application.* 1. Allez sur votre compte Google > Sécurité  
        2. Activez la validation en 2 étapes  
        3. Créez un 'Mot de passe d'application'  
        """)
        email_exp = st.text_input("Votre adresse Gmail", placeholder="exemple@gmail.com")
        mdp_exp = st.text_input("Mot de passe d'application (16 lettres)", type="password", placeholder="abcdefghijklmnop")

    st.header("1️⃣ Préparez votre candidature")
    col1, col2 = st.columns([1, 1])

    with col1:
        cv_file = st.file_uploader("Chargez votre CV au format PDF", type="pdf")

    with col2:
        st.info("💡 Utilisez les balises **{entreprise}** et **{contact}** dans le texte. Si vous n'avez pas de fichier Excel, l'outil tentera de deviner le nom de l'entreprise grâce à l'e-mail !")
        objet_email = st.text_input("Objet de l'email", value="Candidature spontanée stage - {entreprise}")
        corps_email = st.text_area("Corps du message", height=200, value="Bonjour {contact},\n\nJe vous contacte car je suis très intéressé par {entreprise}...")

    st.header("2️⃣ Ajoutez vos contacts")
    tab1, tab2 = st.tabs(["📋 Coller du texte", "📁 Importer un fichier (Excel/CSV)"])

    destinataires_finaux = []

    with tab1:
        texte_brut = st.text_area("Collez vos adresses emails ici :", height=150)
        if texte_brut:
            destinataires_finaux.extend(extraire_emails_simples(texte_brut))

    with tab2:
        st.caption("Votre fichier doit idéalement contenir les colonnes : **Email**, **Entreprise**, et **Contact**.")
        fichier_upload = st.file_uploader("Chargez un fichier contenant vos contacts", type=["xlsx", "csv"])
        
        if fichier_upload is not None:
            try:
                if fichier_upload.name.endswith('.csv'):
                    df = pd.read_csv(fichier_upload)
                else:
                    df = pd.read_excel(fichier_upload)
                
                df.columns = [str(c).strip().lower() for c in df.columns]
                
                if 'email' in df.columns:
                    for index, row in df.iterrows():
                        email = str(row['email']).strip()
                        if pd.notna(email) and "@" in email:
                            entreprise = str(row['entreprise']).strip() if 'entreprise' in df.columns and pd.notna(row['entreprise']) else ""
                            
                            if not entreprise or entreprise == "nan":
                                entreprise = deviner_entreprise_depuis_email(email)
                                
                            contact = str(row['contact']).strip() if 'contact' in df.columns and pd.notna(row['contact']) else ""
                            
                            destinataires_finaux.append({
                                "email": email,
                                "entreprise": entreprise,
                                "contact": contact
                            })
                else:
                    st.warning("Aucune colonne nommée 'Email' trouvée. Extraction basique en cours...")
                    texte_fichier = df.to_csv(index=False)
                    destinataires_finaux.extend(extraire_emails_simples(texte_fichier))
                    
            except Exception as e:
                st.error(f"Erreur de lecture du fichier : {e}")

    emails_vus = set()
    liste_propre = []
    for dest in destinataires_finaux:
        if dest["email"] not in emails_vus:
            emails_vus.add(dest["email"])
            liste_propre.append(dest)
            
    destinataires_finaux = liste_propre

    if destinataires_finaux:
        st.success(f"✅ L'outil a détecté **{len(destinataires_finaux)}** contact(s) unique(s).")
        with st.expander("Voir la liste complète (avec extraction automatique)"):
            st.dataframe(pd.DataFrame(destinataires_finaux), use_container_width=True)

    st.header("3️⃣ Lancer la campagne")
    if st.button("▶️ Envoyer les candidatures", type="primary", use_container_width=True):
        if not email_exp or not mdp_exp:
            st.error("⚠️ Veuillez remplir vos identifiants Gmail dans la barre latérale.")
        elif not cv_file:
            st.error("⚠️ Veuillez charger votre CV.")
        elif not objet_email.strip() or not corps_email.strip():
            st.error("⚠️ L'objet et le corps du message ne peuvent pas être vides.")
        elif len(destinataires_finaux) == 0:
            st.error("⚠️ Aucun email n'a été détecté.")
        else:
            cv_data = cv_file.read()
            cv_name = cv_file.name
            
            progres = st.progress(0)
            status_text = st.empty()
            eta_text = st.empty()
            
            try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login(email_exp, mdp_exp)
                
                count = 0
                total = len(destinataires_finaux)
                
                for dest in destinataires_finaux:
                    msg = EmailMessage()
                    
                    obj_final = objet_email.replace("{entreprise}", dest["entreprise"]).replace("{contact}", dest["contact"]).strip()
                    corps_final = corps_email.replace("{entreprise}", dest["entreprise"]).replace("{contact}", dest["contact"]).strip()
                    
                    obj_final = obj_final.replace(" -  ", "").replace("  ", " ").replace(" -", "")
                    corps_final = corps_final.replace("Bonjour ,", "Bonjour,").replace("Bonjour  ,", "Bonjour,")
                    
                    msg['Subject'] = obj_final
                    msg['From'] = email_exp
                    msg['To'] = dest["email"]
                    msg.set_content(corps_final)
                    msg.add_attachment(cv_data, maintype='application', subtype='pdf', filename=cv_name)
                    
                    server.send_message(msg)
                    
                    count += 1
                    progres.progress(count / total)
                    status_text.success(f"Envoi réussi à {dest['email']} ({count}/{total})")
                    
                    if count < total:
                        temps_restant = (total - count) * 10 
                        minutes, secondes = divmod(temps_restant, 60)
                        eta_text.caption(f"Pause. Temps restant estimé : {minutes} min {secondes} s")
                        time.sleep(random.randint(5, 15))
                    else:
                        eta_text.empty()
                
                server.quit()
                st.balloons()
                st.success(f"🎉 Félicitations ! {count} candidatures envoyées avec succès.")
                
            except Exception as e:
                st.error(f"Une erreur de connexion est survenue : {e}")
                st.warning("Vérifiez que votre 'Mot de passe d'application' est correct et sans espaces.")