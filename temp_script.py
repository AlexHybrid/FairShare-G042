import os, glob

fd = r'c:\FairShare\FairShare-G042\frontend'
html_files = glob.glob(os.path.join(fd, '*.html'))

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('href="styles.css"', 'href="css/styles.css"')
    content = content.replace('href="agreement.css"', 'href="css/agreement.css"')
    content = content.replace('href="listing.css"', 'href="css/listing.css"')
    
    content = content.replace('src="app.js"', 'src="js/app.js"')
    content = content.replace('src="auth.js"', 'src="js/auth.js"')
    content = content.replace('src="announcements.js"', 'src="js/announcements.js"')
    content = content.replace('src="export.js"', 'src="js/export.js"')
    content = content.replace('src="listing.js"', 'src="js/listing.js"')
    content = content.replace('src="payment.js"', 'src="js/payment.js"')
    
    content = content.replace('src="demo.webp"', 'src="assets/demo.webp"')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print('HTML files updated successfully.')
