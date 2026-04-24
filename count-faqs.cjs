const fs = require('fs');
const c = fs.readFileSync('src/data/sampleData.js', 'utf8');
const matches = [...c.matchAll(/f\('m-([^']+)'/g)];
const counts = {};
for (const m of matches) {
  counts[m[1]] = (counts[m[1]] || 0) + 1;
}
Object.entries(counts).sort((a, b) => b[1] - a[1]).forEach(([k, v]) => console.log(k + ': ' + v + ' FAQs'));
console.log('---');
console.log('Total machines:', Object.keys(counts).length);
console.log('Total FAQs:', Object.values(counts).reduce((a, b) => a + b, 0));
