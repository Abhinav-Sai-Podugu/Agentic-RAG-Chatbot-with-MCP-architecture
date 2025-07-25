from uuid import uuid4
from datetime import datetime

def create_mcp_message(sender, receiver, msg_type, payload, trace_id=None):
    return {
        "sender": sender,
        "receiver": receiver,
        "type": msg_type,
        "trace_id": trace_id or str(uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "payload": payload
    }
