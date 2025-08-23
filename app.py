from flask import Flask, render_template, request, session
import re
import tldextract

app = Flask(__name__)
app.secret_key = "supersecretkey" 
def analyze_url(url):    if re.match(r'http[s]?://\d+\.\d+\.\d+\.\d+', url):
        return "⚠️ Not Safe: Possible Malware Host (IP-based domain)"
    phishing_words = ['login', 'verify', 'bank', 'account', 'secure', 'paypal']
    malware_words = ['download', 'exe', 'update', 'install']
spam_words = ['free', 'gift', 'win', 'bonus', 'lottery', 'click']

    if any(word in url.lower() for word in phishing_words):
        return "❌ Not Safe: Phishing attempt"
    elif any(word in url.lower() for word in malware_words):
        return "❌ Not Safe: Malware / Virus distribution"
    elif any(word in url.lower() for word in spam_words):
        return "❌ Not Safe: Spam / Scam link"
    extracted = tldextract.extract(url)
    if extracted.subdomain and extracted.subdomain.count('.') > 1:
        return "⚠️ Not Safe: Suspicious domain structure"

    return "✅ Safe"

@app.route("/", methods=["GET", "POST"])
def home():
    if "history" not in session:
        session["history"] = []

    result = None
    if request.method == "POST":
        url = request.form["url"]
        result = analyze_url(url)

        session["history"].append({"url": url, "result": result})
        session.modified = True

    return render_template("index.html", result=result, history=session["history"])

if __name__ == "__main__":
    app.run(debug=True)

