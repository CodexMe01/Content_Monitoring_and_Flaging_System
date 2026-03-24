from django.utils.dateparse import parse_datetime
from .models import Keyword, ContentItem, Flag

def calculate_score(keyword_name, title, body):
    keyword_name = keyword_name.lower()
    title = title.lower()
    body = body.lower()
    
    score = 0
    if keyword_name == title:
        score = 100
    elif keyword_name in title:
        score = max(score, 70)
    elif keyword_name in body:
        score = max(score, 40)
        
    return score

def scan_content_item(content_dict):
    
    title = content_dict.get('title')
    source = content_dict.get('source')
    body = content_dict.get('body')
    new_last_updated_str = content_dict.get('last_updated')
    new_last_updated = parse_datetime(new_last_updated_str) if new_last_updated_str else None

    
    item = ContentItem.objects.filter(title=title, source=source).first()
    content_changed = False

    if item:
        
        if new_last_updated and item.last_updated:
            if new_last_updated > item.last_updated:
                content_changed = True
        else:
            if body != item.body:
                content_changed = True

        if content_changed:
            item.body = body
            if new_last_updated:
                item.last_updated = new_last_updated
            item.save()
    else:
        item = ContentItem.objects.create(
            title=title, 
            source=source, 
            body=body, 
            last_updated=new_last_updated
        )
        content_changed = True

    keywords = Keyword.objects.all()
    flags_processed = []

    for kw in keywords:
        score = calculate_score(kw.name, item.title, item.body)
        if score > 0:
            flag = Flag.objects.filter(keyword=kw, content_item=item).first()
            if flag:
                if flag.status == 'irrelevant':
                    if content_changed:
                        flag.status = 'pending'
                        flag.score = score
                        flag.save()
                        flags_processed.append(flag)
                else:
                    if content_changed:
                        flag.score = score
                        flag.save()
                        flags_processed.append(flag)
            else:
                flag = Flag.objects.create(
                    keyword=kw, content_item=item, score=score
                )
                flags_processed.append(flag)
                
    return flags_processed
