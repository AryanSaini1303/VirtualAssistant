if appName=="video":
            text=text.lower().replace("prime video","primevideo")
            appList=re.findall(pattern,text)
            for x in appList:
                appName=x