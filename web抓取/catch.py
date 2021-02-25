# -*- coding: utf-8 -*-
import json  
import urllib  
import urllib2  
import os   
  
MD5 = "FF1A3887487F9E345DF7910C2AD919DF"  
#MD5 = "12fa5fb74201d9b6a14f63fbf9a81ff6"  #do not have report on virustotal.com   
  
  
              
########################################################################   
APIKEY = "e45b231768689a6a1e46d2edf36073a17fdf1ab93058f1f5b32bc8bc7e4d57fe"#  这里用你自己在virustotal上申请的账号的KEY"  
  
  
class VirusTotal:  
    """"""  
  
    #----------------------------------------------------------------------   
    def __init__(self, md5):  
        """Constructor"""  
        self._virus_dict = {}  
        self._md5 = md5  
          
          
    def repr(self):  
        return str(self._virus_dict)  
      
    def submit_md5(self, file_path):  
        import postfile                                                                            
        #submit the file   
        FILE_NAME =  os.path.basename(file_path)   
                             
                                                                                                   
        host = "www.virustotal.com"                                                                
        #selector = "https://www.virustotal.com/vtapi/v2/file/scan"
        selector = "https://www.virustotal.com/en/search/"                                  
        fields = [("apikey", APIKEY)]  
        file_to_send = open(file_path, "rb").read()                                                
        files = [("file", FILE_NAME, file_to_send)]                                                
        json = postfile.post_multipart(host, selector, fields, files)                              
        print json  
        pass  
      
    def get_report_dict(self):  
        result_dict = {}  
          
        url = "https://www.virustotal.com/en/file/b397dfdcb056c3c927f158590604e8aa8eb7b6785ea70ada7a5ecb31ae0d8db5/analysis/"  
        parameters = {"resource": self._md5,  
                       "apikey": APIKEY}  
        data = urllib.urlencode(parameters)  
        req = urllib2.Request(url, data)  
        response = urllib2.urlopen(req)  
        json = response.read()  
          
        response_dict = json.loads(json)  
        if response_dict["response_code"]: #has result    
            scans_dict = response_dict.get("scans", {})  
            for anti_virus_comany, virus_name in scans_dict.iteritems():  
                if virus_name["detected"]:  
                    self._virus_dict.setdefault(anti_virus_comany, virus_name["result"])  
        return self._virus_dict  
              
          