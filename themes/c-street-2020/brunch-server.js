const express = require('express');
const app = express();

app.use('themes/c-street-2020', express.static(__dirname));
app.use('files', express.static(__dirname + '/mock/files'));
app.use('static', express.static(__dirname + '/mock/static'));
app.use('/', express.static(__dirname + '/mock'));

// AJAX to /action.
app.post('/action', (req, res, next) => {
  res.send('POST action completed!');
});

// Export the module like this for Brunch.
module.exports = (config, callback) => {
  // Server config is passed within the `config` variable.
  app.listen(config.port, function () {
    console.log(`Test server listening on port ${config.port}!`);
    console.log(JSON.stringify(config));
    console.log(app.mountpath);
    callback();
  });

  // Return the app; it has the `close()` method, which would be ran when
  // Brunch server is terminated
  return app;
};
