import re
import requests
import json

def get_urls_for_pages(url:str, start_page:int=1, pages:int=1, stop:str='', allow_repeat:bool=False)->list|tuple:
    '''
    function make requests for an url with different pages: till get pages cap or get an stop-sequence
    autonomic function can take for a while...[in case of slow implementation]
        params:
            url(str): url to use with page iterator
                for dynamic iterations u must check how pages' iteration is set. Iterator is set by '{page}'. if no iteration found it would be url->url/1->url/2 by default
                exp: 'some_url.com/{page}'-> sill set iterations on {page} and we get 'some_url.com/1', 'some_url.com/2', etc... 
            start_page(int|default=1): start page for iterations 
            pages(int|default=1): precision count of pages to unpack. if pages is set to 0 will try to get all pages: be careful to check if allow_repeat==False or stop is set!
            stop(any|default=''): a stop-sequence to stop iterations may be any object that can be converted to str
            allow_repeat(bool|default=False): a setting that allow repeatable pages
        returns:
            urls(list): list of urls for pages or tuple(None, str(exception)) if something goes wrong
    !ATTENTION function may work for infinity if stop or pages would not be set correct and allow_repeat==True!
    exp:get_urls_for_pages(url, 1, 3) -> return 3 url:[url/1, url/2, ur/3] from page 1 till 3
    exp:get_urls_for_pages(url) -> return 1 url:[url/1] -> 1 page from page 1 it's trully page one
    exp:get_urls_for_pages(url, 1, 0, 'page not found') -> return 3 url:[url/1, url/2, ur/3, ...] from page 1 till stop-seq not found
    exp:get_urls_for_pages(url, pages=0) -> return 3 url:[url/1, url/2, ur/3, ...] from page 1 till repeatable pages   
    '''
    if '{page}' not in url:
        if url[-1]!='/':
            url+='/'
        url+='{page}'
    if pages<1 and pages != 0:
        return (None, 'wrong pages count<1 and pages!=0')
    urls=[]
    if pages==0 or stop!='':
        iterator=start_page        
        if allow_repeat:
            while True:
                request=requests.get(url.replace('{page}',str(iterator))).text
                if stop!='' and stop in request:
                    break
                urls.append(url.replace('{page}', str(iterator)))
                iterator+=1
        else:
            request_second=''
            iterator=start_page 
            while True:
                request_first=requests.get(url.replace('{page}', str(iterator))).text
                if stop!='' and stop in request_first:
                    break
                if request_first!=request_second:
                    urls.append(url.replace('{page}', str(iterator)))
                    request_second=request_first
                else:
                    break
                iterator+=1
    else:
        if allow_repeat:
            for iterator in range(start_page, start_page+pages):
                request=requests.get(url.replace('{page}',str(iterator))).text
                if stop!='' and stop in request:
                    break
                urls.append(url.replace('{page}', str(iterator)))
        else:
            request_second=''
            for iterator in range(start_page, start_page+pages):
                request_first=requests.get(url.replace('{page}', str(iterator))).text
                if stop!='' and stop in request_first:
                    break
                if request_first!=request_second:
                    urls.append(url.replace('{page}', str(iterator)))
                    request_second=request_first
                else:
                    break
    return urls  

def analyze(*urls:str|list)->dict:
    '''
    returns dict of all possible tags that can be used as patterns of parsing on current url-page
        params:
            url(s):tuple(str)|str - url(s) to find a patterns
        result:
            possible_patterns(dict): a dictionary of all tags and html schema to parse optionally
    structure of possible_patterns:{
    'tags':
        'tag1': [meta1, meta2,...] #(meta is like class or charset or smth else in tag construction)
        'tag2': [meta1, meta2,...] #(meta is like class or charset or smth else in tag construction)
        ...
    [WIP another types of analysis such as html-schema or smth else]    
    '''
    possible_patterns={}
    if type(urls[0])==list:
        urls=tuple(urls[0])
    if len(urls)!=1:
        for url in urls:
            possible_patterns_url = analyze(url)
            possible_patterns.update(possible_patterns_url)
    else:
        url = urls[0]
    html_str=requests.get(url).text
    tags_text = html_str
    possible_patterns[tags_text.split('\n')[0]]=[]
    tags_text=tags_text.replace("\t", "").replace("\n", "").split('<!DOCTYPE')[1]
    tags={}
    possible_patterns['js']=False
    while re.search(r'<.*?>',tags_text)!=None:
        tag=re.search(r'<.*?>',tags_text).group().replace(' ', '###|###',1).split('###|###')
        props = [] 
        if '<!--' not in tag[0]:
            try:            
                tag_prop=tag[1]
                props=re.findall(r'([^"]*?)=',tag_prop)            
            except: pass
            finally:
                tag = tag[0].replace(' ', '')
                if tag[-1]!=">":
                    tag_name=tag.replace('/', '').split(' ')[0]+'>'
                    if tag_name not in tags.keys():
                        tags[tag_name]=props
                    else:
                        props = props+tags[tag_name]
                        tags.update({tag_name:props})
                else:
                    tags[(tag.replace('/', ''))] = props            
            tags_text = tags_text.replace(tag,'').replace(f"/{tag}", '')  
        else:  
            possible_patterns['js']=True
            tags_text = tags_text.replace(tag[0],'')
    possible_patterns['tags']=tags 
    return possible_patterns

def return_special_chars(text:str)->str:
    '''
    returns text with readable special-html-chars like ' and so on
    '''
    char_dict={
        '&#34;':'"',
        '&#38;':'&',
        '&#39;':"'",
        '&#60;':'<',
        '&#62;':'>',
        '“':'"',
        '”':'"',
        }
    for code, char in char_dict.items():
        text=text.replace(code, char)
    return text

def parse(patterns_to_parse:str|dict, str_to_parse:str, alias:list[str]=[], regexp=True, group_by:str='pattern')->dict:
    '''
    returns parse-dictionary of parsed string
        params:
            pattern_to_pars(str|dict): pattern used to be a schema-string to get info from parsing-string
            str_to_parse(str): must be string or url-string->to parse some domen
            alias(list(str)): alias for patterns
            regexp(bool|default=True): parsing method. if True all the patterns will be used as regExp patterns
            group_by(str|default='pattern'): grouping method: 'pattern' will group parsing around pattern, 'iteration' will group parsing by all-the-patterns iterations
        result:
            parsed_dict(dict): dictionary of parsed thing that match pattern
                view of parsed_dict:{1(or alias1):[match1, match2,...], 2(or alias2)[...], ...}
    '''    
    url=re.sub(r'https?://[a-zA-Z0-9./?&=_-]+','',str_to_parse, 1)
    if url=='':
        text=requests.get(str_to_parse).text
    else:
        text=str_to_parse
    if group_by=='pattern':
        parsed_dict=dict.fromkeys(patterns_to_parse) 
        if regexp:
            for pattern in patterns_to_parse:
                parsed_dict[pattern]=[]
                while re.search(pattern, text)!=None:
                    part=re.search(pattern, text)
                    parsed_dict[pattern].append(return_special_chars(re.sub(r'\s+',' ',part.group(1))))
                    text=text.replace(part.group(),'',1)
        else: raise Exception('Not implemented yet')
    if group_by=='iteration':
        parsed_dict={}
        if regexp:
            iterator=1
            iteration=0
            while iterator!=0:
                iterator=0                
                parsed_dict[iteration]=dict.fromkeys(patterns_to_parse)
                for pattern in patterns_to_parse:
                    part=re.search(pattern, text)
                    parsed_dict[iteration][pattern] = return_special_chars(re.sub(r'\s+',' ',part.group(1)))
                    text=text.replace(part.group(),'',1)
                    if re.search(pattern, text)!=None:
                        iterator+=1                    
                iteration+=1                
        else: raise Exception('Not implemented yet')
    if len(alias)>len(patterns_to_parse) or alias==[]:
        return parsed_dict
    else:
        if group_by=='pattern':
            iterator=0
            for alia in alias:
                parsed_dict[alia]=parsed_dict.pop(patterns_to_parse[iterator])
                iterator+=1
        elif group_by=='iteration':
            count=len(parsed_dict.items())
            for iteration in range(0, count):
                iterator=0
                for alia in alias:
                    parsed_dict[iteration][alia]=parsed_dict[iteration].pop(patterns_to_parse[iterator])
                    iterator+=1
        return parsed_dict

patterns=[r'itemprop="text">(.*?)<',r'itemprop="author">(.*?)<',r'itemprop="keywords" content="(.*?)".*?>']
parsed_pages={}
for url in get_urls_for_pages('https://quotes.toscrape.com/page/', stop='No quotes found'):
    parsed_pages[f'{url}']=parse(patterns, url, ['Text', 'Author', 'Tags'], group_by='iteration')
print(parsed_pages)
with open("data.json", "w") as json_file:
    json.dump(parsed_pages, json_file, indent=4)
