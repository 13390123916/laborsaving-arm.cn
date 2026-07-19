/* 文章富文本辅助工具栏 - 原生 JS，无第三方依赖
 * 在 Django Admin 的 content 文本域上方注入格式化按钮，
 * 直接写入标准 HTML（<h2>/<p>/<strong>/<ul>/<a>/<img>），
 * 前端详情页以 v-html 渲染，支持图文混排。
 */
(function () {
  'use strict';

  function initRichText() {
    var ta = document.getElementById('id_content');
    if (!ta || ta.dataset.richtextReady) return;
    ta.dataset.richtextReady = '1';

    var wrap = document.createElement('div');
    wrap.className = 'rt-toolbar';
    wrap.style.margin = '6px 0';

    function wrapTag(tag, attr) {
      var start = ta.selectionStart, end = ta.selectionEnd;
      var sel = ta.value.substring(start, end) || '内容';
      var open = attr ? '<' + tag + ' ' + attr + '>' : '<' + tag + '>';
      var text = open + sel + '</' + tag + '>';
      ta.value = ta.value.substring(0, start) + text + ta.value.substring(end);
      ta.focus();
    }

    function insertAtCursor(html) {
      var start = ta.selectionStart, end = ta.selectionEnd;
      ta.value = ta.value.substring(0, start) + html + ta.value.substring(end);
      ta.focus();
    }

    var buttons = [
      { label: '标题', fn: function () { wrapTag('h2'); } },
      { label: '段落', fn: function () { wrapTag('p'); } },
      { label: '加粗', fn: function () { wrapTag('strong'); } },
      { label: '列表', fn: function () { wrapTag('ul'); } },
      { label: '链接', fn: function () {
          var url = prompt('请输入链接地址：', 'https://');
          if (url) wrapTag('a', 'href="' + url + '"');
        } },
      { label: '图片', fn: function () {
          var url = prompt('请输入图片地址（可在「媒体图库」上传后复制链接）：', '/media/uploads/');
          if (url) insertAtCursor('<img src="' + url + '" alt="图片" style="max-width:100%;border-radius:8px;" />');
        } },
      { label: '横线', fn: function () { insertAtCursor('<hr />'); } }
    ];

    buttons.forEach(function (b) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.textContent = b.label;
      btn.className = 'rt-btn';
      btn.addEventListener('click', b.fn);
      wrap.appendChild(btn);
    });

    ta.parentNode.insertBefore(wrap, ta);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initRichText);
  } else {
    initRichText();
  }
})();
