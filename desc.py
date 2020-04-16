import json

fp = open("table.json", "r")
table_json = json.loads(fp.read())
fp.close()

SKIP_OVERWRITE = input("skip to empty description? (y/n): ")[0].lower() == "y"
def overwrite_desc(item):
    if not SKIP_OVERWRITE: return True
    else: return item.get("desc", "")

for mod_name in table_json.keys():
    item = table_json[mod_name]
    if not overwrite_desc(item):
        print("Please enter a description for " + mod_name + " (type in !quit to escape)")
        desc = ""
        while desc[-7:] != '!quit\n\n': 
            desc += input() + "\n\n"
        desc = desc[:-7]
        desc = desc.replace("> ", "")
        if desc: item["desc"] = desc
        image = input("Enter a link to an image, or just press enter to skip: ")
        if image: item["image"] = image

        print("saving description...")
        fp = open("table.json", "w")
        json.dump(table_json, fp, indent=4)
        fp.close()
