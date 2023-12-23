// Last modified: 23/12/2023 19:28 by Draggie306
// Converts Kaspersky Password Manager export to Chromium Password Manager CSV export

// Permission is granted to anyone to use this software for any purpose, including commercial applications, providing that the following conditions are met:
// 1. Give appropriate credit, provide a link to the original source (https://github.com/Draggie306/kaspersky-to-csv) and indicate if changes were made.
// 2. Do not use this software for illegal purposes.
// 3. If you find a bug, report it to me so I can fix it.
// 4. If you make any changes, you must release them under the same license.
// 5. Do not claim this software as your own.
// 6. Have fun!

// on DOM load
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('Status').innerHTML = 'Status: Ready';

    // Ensure the element exists before attaching event listener
    var convertButton = document.getElementById('convertButton');
    if (convertButton) {
        convertButton.addEventListener('click', function() {
        var accountCount = 0;
        var countOfAccounts = document.getElementById('countOfAccounts');
        var fileInput = document.getElementById('fileInput');
        var file = fileInput.files[0];
        var reader = new FileReader();
        reader.onload = function(e) {
            var lines = e.target.result.split('\n');
            var websites = [];
            var i = 0;
            while (i < lines.length) {
                var line = lines[i].trim();
                if (line.includes('Websites')) {
                    i++;
                    while (i < lines.length && !lines[i].includes('Applications')) {
                        if (lines[i].includes('---')) {
                            i++;
                            continue;
                        }
                        var record = {};
                        while (i < lines.length && !lines[i].includes('---')) {
                            // holy this is ugly
                            if (lines[i].includes('Website name:')) {
                                let value = lines[i].split(':', 2)[1].trim();
                                record['Website name'] = `"${value.replace(/"/g, '""')}"`;
                            } else if (lines[i].includes('Website URL:')) {
                                let fixed_url = lines[i].replace('Website URL: ', '').trim();
                                if (!fixed_url.startsWith('http')) {
                                    fixed_url = 'https://' + fixed_url;
                                }
                                record['Website URL'] = `"${fixed_url}"`;
                                // record['Website URL'] = `"${lines[i].replace('Website URL: ', '').trim()}"`;
                            } else if (lines[i].includes('Login:')) {
                                let value = lines[i].split(':', 2)[1].trim();
                                record['Login'] = `"${value.replace(/"/g, '""')}"`;
                            } else if (lines[i].includes('Password:')) {
                                let value = lines[i].split(':').slice(1).join(':').trim();
                                record['Password'] = `"${value.replace(/"/g, '""')}"`;
                            } else if (lines[i].includes('Application:')) {
                                let value = lines[i].split(':', 2)[1].trim();
                                record['Application'] = `"${value.replace(/"/g, '""')}"`;
                            } else if (lines[i].includes('Comment:')) {
                                let value = lines[i].split(':', 2)[1].trim();
                                record['Comment'] = `"${value.replace(/"/g, '""')}"`;
                            }
                            i++;
                        }
                        accountCount++;
                        countOfAccounts.innerHTML = `Accounts found: ${accountCount}`;
                        websites.push(record);
                    }
                }
                i++;
            }
            var csvContent = 'name,url,username,password,note,isApplication\n';
            for (var website of websites) {
                var note = website['Comment'] || '';
                if (website['Website name'] && website['Website URL']) {
                    csvContent += `${website['Website name']},${website['Website URL']},${website['Login']},${website['Password']},${note},false\n`;
                } else if (website['Application']) {
                    csvContent += `${website['Application']},,${website['Login']},${website['Password']},${note},true\n`;
                }
            }
            var blob = new Blob([csvContent], {type: 'text/csv'});
            var url = URL.createObjectURL(blob);
            var downloadLink = document.getElementById('downloadLink');
            downloadLink.href = url;
            downloadLink.download = 'kaspersky_export.csv';
            downloadLink.click();
        };
        reader.readAsText(file);
        }
    )}
}
);
