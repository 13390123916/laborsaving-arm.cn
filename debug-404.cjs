/* 精确捕获失败请求 URL（路径基于脚本自身位置，克隆到任意目录均可运行） */
const path = require('path')
const puppeteer = require(path.resolve(__dirname, 'frontend/node_modules/puppeteer-core'))
const { spawn } = require('child_process')
const { execSync } = require('child_process')
const ROOT = __dirname
const CHROME_BIN = '/usr/bin/chromium'
const HOST = '127.0.0.1', PREVIEW_PORT = 4173, API = 'http://127.0.0.1:8000'

async function waitServer(url, t=40){for(let i=0;i<t;i++){try{execSync(`curl -s -o /dev/null ${url}`);return}catch(e){}await new Promise(r=>setTimeout(r,500))}}

async function main(){
  const backend = spawn('python3',['manage.py','runserver',`${HOST}:8000`],{cwd:path.resolve(ROOT,'backend'),stdio:'ignore',detached:true})
  const preview = spawn('pnpm',['exec','vite','preview','--host',HOST,'--port',String(PREVIEW_PORT),'--strictPort'],{cwd:path.resolve(ROOT,'frontend'),stdio:'ignore',detached:true,shell:true})
  await waitServer(`${API}/api/site-config/info/`); await waitServer(`http://${HOST}:${PREVIEW_PORT}/`)
  const browser = await puppeteer.launch({executablePath:CHROME_BIN,headless:'new',args:['--no-sandbox','--disable-dev-shm-usage']})
  for(const route of ['/','/about']){
    const page = await browser.newPage()
    const failed=[]
    page.on('requestfailed', r=>failed.push(`FAIL ${r.failure().errorText} ${r.url()}`))
    page.on('response', r=>{ if(r.status()>=400) failed.push(`HTTP ${r.status()} ${r.url()}`) })
    await page.goto(`http://${HOST}:${PREVIEW_PORT}${route}`,{waitUntil:'networkidle0',timeout:30000})
    await new Promise(r=>setTimeout(r,2000))
    console.log(`\n===== ${route} failed resources (${failed.length}) =====`)
    failed.forEach(f=>console.log(' ',f))
    await page.close()
  }
  await browser.close()
  try{process.kill(-backend.pid)}catch(e){}
  try{process.kill(-preview.pid)}catch(e){}
  console.log('\n[done]')
}
main().catch(e=>{console.error('FATAL',e);process.exit(1)})
