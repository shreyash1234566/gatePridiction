import json
import re
from difflib import SequenceMatcher

def normalize(text):
    if not isinstance(text, str):
        return ""
    # Convert all labels to lowercase, trim spaces, remove special characters like '(', ')', '/', '-'
    text = text.lower().strip()
    text = re.sub(r'[\(\)\/\-]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def main():
    try:
        with open("Q.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print("Error loading Q.json:", e)
        return

    hist_micro = set()
    new_micro = set()

    for q in data:
        year = q.get("year", 0)
        micro = q.get("micro_topic", "")
        if not micro:
            continue
        
        # In case micro_topic is a list or string
        if isinstance(micro, list):
            micros = micro
        else:
            micros = [micro]
        
        for m in micros:
            if year < 2026:
                hist_micro.add(m)
            elif year == 2026:
                new_micro.add(m)
                
    # Filter for "first-seen" in 2026: new_micro - hist_micro (based on exact match first?)
    # The prompt says "Audit the 40 'first-seen' microtopics from 2026".
    # Let's find exactly which ones have not been seen in < 2026 (exact match of original strings or normalized?).
    
    first_seen = [m for m in new_micro if m not in hist_micro]
    
    print(f"Total historical microtopics: {len(hist_micro)}")
    print(f"Total new microtopics in 2026: {len(new_micro)}")
    print(f"First-seen original strings in 2026: {len(first_seen)}")
    
    # Store normalized versions
    norm_hist = {normalize(h): h for h in hist_micro}
    
    results = []
    
    for m in first_seen:
        norm_m = normalize(m)
        
        best_match = None
        best_score = 0
        best_orig = None
        
        for norm_h, orig_h in norm_hist.items():
            score = SequenceMatcher(None, norm_m, norm_h).ratio()
            if score > best_score:
                best_score = score
                best_match = norm_h
                best_orig = orig_h
                
        results.append({
            "FirstSeen2026": m,
            "NormFirstSeen": norm_m,
            "BestMatchHist": best_orig,
            "NormBestMatch": best_match,
            "Score": best_score
        })
        
    results.sort(key=lambda x: x["Score"], reverse=True)
    
    print("-" * 120)
    print(f"{'2026 Observed':<45} | {'Historically Similar Label':<45} | {'Score':<5}")
    print("-" * 120)
    for r in results:
        print(f"{r['FirstSeen2026'][:45]:<45} | {r['BestMatchHist'][:45]:<45} | {r['Score']:.2f}")

    print("\nBased on the table, the ones with Score > 0.85 really look like they should have been mapped to existing ones.")

main()
