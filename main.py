import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="OSINT Dashboard – By Anis",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 OSINT Username Recon Dashboard")
st.subheader("Ethical OSINT Tool – By Anis")
st.markdown("---")

user_input = st.text_input(
    "👤 أدخل Username واحد أو عدة (مفصولة بفاصلة)",
    placeholder="anis, root, admin"
)

scan_btn = st.button("🚀 Scan")

sites = {
    "GitHub": "https://github.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "Twitter": "https://twitter.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "TikTok": "https://www.tiktok.com/@{}",
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

if scan_btn and user_input:
    usernames = [u.strip() for u in user_input.split(",")]
    results = []

    with open("results.txt", "a", encoding="utf-8") as f:
        for username in usernames:
            st.markdown(f"### 🔎 Results for `{username}`")
            f.write(f"\nResults for {username}\n")

            for site, url in sites.items():
                try:
                    r = requests.get(url.format(username), headers=headers, timeout=5)
                    if r.status_code == 200:
                        status = "FOUND"
                        st.success(f"{site}: موجود ✅")
                    else:
                        status = "NOT FOUND"
                        st.error(f"{site}: غير موجود ❌")
                except:
                    status = "ERROR"
                    st.warning(f"{site}: خطأ اتصال ⚠️")

                results.append({
                    "Username": username,
                    "Site": site,
                    "Status": status
                })
                f.write(f"[{status}] {site}\n")

    df = pd.DataFrame(results)
    st.markdown("---")
    st.subheader("📊 Results Table")
    st.dataframe(df)

    st.info("📁 تم حفظ النتائج في ملف results.txt")