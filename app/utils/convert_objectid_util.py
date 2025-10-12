from bson import ObjectId

def convert_objectid(doc):
    if isinstance(doc, list):
        return [convert_objectid(i) for i in doc]
    
    if isinstance(doc, dict):
        new_doc = {}
        for k, v in doc.items():
            if k == "password":
                continue
            if k == "_id":
                new_doc["id"] = convert_objectid(v)
            else:
                new_doc[k] = convert_objectid(v)
        return new_doc
    
    if isinstance(doc, ObjectId):
        return str(doc)
    
    return doc
