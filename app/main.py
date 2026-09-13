from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from urllib.parse import urlparse

import joblib
import pandas as pd

from app.feature_extractor import extract_features, normalize_url


app = FastAPI(
    title="Phishing URL Detection"
)

templates = Jinja2Templates(
    directory="app/templates"
)


model = joblib.load(
    "./models/phishing_hgb_normalized.pkl"
)
test_urls = [
    "https://www.apple.com",
    "https://www.apple.com/"
]
#testt
for test_url in test_urls:
    test_features = extract_features(test_url)
    test_df = pd.DataFrame([test_features])

    test_prob = model.predict_proba(test_df)[0]
    phishing_index = list(model.classes_).index(0)

    print("\nTEST URL   :", repr(test_url))
    print("NORMALIZED :", repr(normalize_url(test_url)))
    print("FEATURES   :", test_features)
    print(
        "RISK       :",
        test_prob[phishing_index] * 100
    )
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.post("/predict", response_class=HTMLResponse)
def predict(
    request: Request,
    url: str = Form(...)
):
    features = extract_features(url)

    print("\n====================")
    print("RAW        :", repr(url))
    print("NORMALIZED :", repr(normalize_url(url)))
    print("FEATURES   :", features)
    print("====================")

    features_df = pd.DataFrame([features])

    prediction = model.predict(features_df)[0]

    probabilities = model.predict_proba(features_df)[0]

    phishing_index = list(model.classes_).index(0)

    phishing_probability = probabilities[phishing_index]

    risk_score = round(
        float(phishing_probability) * 100,
        2
    )

    print("PREDICTION :", prediction)
    print("PROBABILITY:", probabilities)
    print("RISK       :", risk_score)

    if prediction == 0:
        result = "Phishing"
    else:
        result = "Legitimate"

    # Confidence = probability of the predicted class
    if result == "Legitimate":
        confidence_score = round(100 - risk_score, 2)
    else:
        confidence_score = risk_score

    # --- Display-friendly URL analysis values ---
    normalized = normalize_url(url)
    parsed = urlparse(normalized)
    domain = parsed.hostname or ""
    domain_parts = domain.split(".")
    tld = "." + domain_parts[-1] if len(domain_parts) > 1 else "N/A"

    display_https = "Yes" if features["IsHTTPS"] == 1 else "No"
    display_url_length = features["URLLength"]
    display_domain_length = features["DomainLength"]
    display_subdomains = features["NoOfSubDomain"]
    display_tld = tld
    display_digits = features["NoOfDegitsInURL"]
    display_special_chars = features["NoOfOtherSpecialCharsInURL"]
    display_domain = domain

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "url": url,
            "result": result,
            "risk_score": risk_score,
            "confidence_score": confidence_score,
            "display_https": display_https,
            "display_url_length": display_url_length,
            "display_domain_length": display_domain_length,
            "display_subdomains": display_subdomains,
            "display_tld": display_tld,
            "display_digits": display_digits,
            "display_special_chars": display_special_chars,
            "display_domain": display_domain,
        }
    )