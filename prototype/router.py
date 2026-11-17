"""Step 1 — the router (rung 1: rules), spec §2.1. Language and amount, before anything else."""
import re

FR_WORDS = {"je", "le", "les", "est", "pas", "mais", "une", "colis", "étiquette", "vous", "jamais", "mon",
            "ma", "demande", "demandé", "remboursement", "remboursé", "non", "depuis", "sur", "même",
            "encore", "livré", "numéro", "cette", "merci", "perdu", "utilisée", "achetée", "transporteur", "svp"}
EN_WORDS = {"the", "my", "was", "is", "i", "please", "label", "parcel", "package", "refund", "never", "not",
            "for", "it", "this", "same", "lost", "delivered", "charged"}


def language(text):
    """Return 'fr', 'en' or 'other' from a word list. Never translates."""
    words = set(re.findall(r"[a-zà-ÿ]+", (text or "").lower()))
    if words & FR_WORDS:
        return "fr"
    if words & EN_WORDS:
        return "en"
    return "other"


def amount(value):
    """Return the amount as a positive number rounded to the cent, or None."""
    try:
        eur = round(float(str(value).replace(",", ".").replace("€", "").strip()), 2)
    except ValueError:
        return None
    return eur if eur > 0 else None


def route(text, amount_eur):
    """Return (language, amount, stop_reason). stop_reason is None when the case can go on."""
    lang, eur = language(text), amount(amount_eur)
    if lang == "other":
        return lang, eur, "language_not_covered"
    if eur is None:
        return lang, eur, "amount_missing"
    return lang, eur, None