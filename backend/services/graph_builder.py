"""
ScamGraph AI - Scam Graph Network Builder
Generates interconnected graph nodes and edges (React Flow compatible)
representing the full scam infrastructure:
Phone/Sender -> Message -> URLs -> Domains -> UPI IDs -> Scam Pattern -> Category.
"""

from typing import Dict, Any, List


def build_scam_graph(
    sender: str,
    text_preview: str,
    entities: Dict[str, Any],
    workflow_events: List[str],
    scam_dna: str,
    category: str
) -> Dict[str, Any]:
    """
    Constructs node-link graph data formatted for React Flow.
    """
    nodes = []
    edges = []

    # Layout coordinates (X, Y)
    curr_x = 250
    curr_y = 50
    y_step = 100

    prev_node_id = None

    # 1. Sender Node (Phone / Email / Unknown)
    sender_val = sender if sender else (entities.get("phone_numbers", ["Unknown Origin"])[0] if entities.get("phone_numbers") else "Unknown Sender")
    sender_id = "node-sender"
    nodes.append({
        "id": sender_id,
        "type": "senderNode",
        "label": f"Sender: {sender_val}",
        "data": {
            "entityType": "phone" if any(c.isdigit() for c in sender_val) else "sender",
            "value": sender_val,
            "badge": "SOURCE"
        },
        "position": {"x": curr_x, "y": curr_y}
    })
    curr_y += y_step
    prev_node_id = sender_id

    # 2. Message Content Node
    msg_id = "node-message"
    nodes.append({
        "id": msg_id,
        "type": "messageNode",
        "label": f"Message: {text_preview[:45]}...",
        "data": {
            "entityType": "message",
            "preview": text_preview,
            "badge": "PAYLOAD"
        },
        "position": {"x": curr_x, "y": curr_y}
    })
    edges.append({
        "id": f"e-{prev_node_id}-{msg_id}",
        "source": prev_node_id,
        "target": msg_id,
        "label": "SENT",
        "animated": True
    })
    curr_y += y_step
    prev_node_id = msg_id

    # 3. URL / Domain Nodes
    urls = entities.get("urls", [])
    if urls:
        for idx, u in enumerate(urls[:2]):
            url_id = f"node-url-{idx}"
            domain = u.replace("http://", "").replace("https://", "").split("/")[0]
            nodes.append({
                "id": url_id,
                "type": "urlNode",
                "label": f"Phishing URL: {domain}",
                "data": {
                    "entityType": "url",
                    "full_url": u,
                    "domain": domain,
                    "badge": "SUSPICIOUS_LINK"
                },
                "position": {"x": curr_x + (idx * 160) - 80, "y": curr_y}
            })
            edges.append({
                "id": f"e-{prev_node_id}-{url_id}",
                "source": prev_node_id,
                "target": url_id,
                "label": "CONTAINS",
                "animated": True
            })
            prev_node_id = url_id
        curr_y += y_step

    # 4. UPI ID Node (if detected)
    upi_ids = entities.get("upi_ids", [])
    if upi_ids:
        for idx, upi in enumerate(upi_ids[:2]):
            upi_node_id = f"node-upi-{idx}"
            nodes.append({
                "id": upi_node_id,
                "type": "upiNode",
                "label": f"UPI Handle: {upi}",
                "data": {
                    "entityType": "upi",
                    "value": upi,
                    "badge": "PAYMENT_TARGET"
                },
                "position": {"x": curr_x + (idx * 160) - 80, "y": curr_y}
            })
            edges.append({
                "id": f"e-{prev_node_id}-{upi_node_id}",
                "source": prev_node_id,
                "target": upi_node_id,
                "label": "TARGETS",
                "animated": True
            })
            prev_node_id = upi_node_id
        curr_y += y_step

    # 5. Scam DNA Pattern Node
    dna_id = "node-scam-dna"
    nodes.append({
        "id": dna_id,
        "type": "patternNode",
        "label": f"Scam DNA: {scam_dna}",
        "data": {
            "entityType": "scam_dna",
            "dna": scam_dna,
            "badge": "CAMPAIGN_FINGERPRINT"
        },
        "position": {"x": curr_x, "y": curr_y}
    })
    edges.append({
        "id": f"e-{prev_node_id}-{dna_id}",
        "source": prev_node_id,
        "target": dna_id,
        "label": "MATCHES",
        "animated": True
    })
    curr_y += y_step
    prev_node_id = dna_id

    # 6. Category Node
    cat_id = "node-category"
    nodes.append({
        "id": cat_id,
        "type": "categoryNode",
        "label": f"Category: {category}",
        "data": {
            "entityType": "category",
            "category": category,
            "badge": "FRAUD_CATEGORY"
        },
        "position": {"x": curr_x, "y": curr_y}
    })
    edges.append({
        "id": f"e-{prev_node_id}-{cat_id}",
        "source": prev_node_id,
        "target": cat_id,
        "label": "BELONGS_TO",
        "animated": False
    })

    return {
        "nodes": nodes,
        "edges": edges
    }
