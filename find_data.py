from bs4 import BeautifulSoup

with open("temp_caratlane_dump.html", "r") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
scripts = soup.find_all("script")

for i, script in enumerate(scripts):
    if script.string and "18 KT" in script.string:
        print(f"Found in script {i}")
        print(script.string[:500]) # Print start of script
