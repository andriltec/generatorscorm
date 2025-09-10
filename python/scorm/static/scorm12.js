(function() {
  function findAPI(win) {
    var findTries = 0;
    while ((win.API == null) && (win.parent != null) && (win.parent != win) && (findTries < 500)) {
      findTries++;
      win = win.parent;
    }
    return win.API || null;
  }

  window.SCORM = {
    api: null,
    init: function() {
      try {
        this.api = findAPI(window);
        if (this.api && this.api.LMSInitialize) {
          this.api.LMSInitialize("");
        }
      } catch(e) {}
    },
    complete: function() {
      try {
        if (this.api && this.api.LMSSetValue) {
          this.api.LMSSetValue('cmi.core.lesson_status', 'completed');
          this.api.LMSCommit("");
        }
      } catch(e) {}
    },
    finish: function() {
      try {
        if (this.api && this.api.LMSFinish) {
          this.api.LMSFinish("");
        }
      } catch(e) {}
    }
  };
})();

