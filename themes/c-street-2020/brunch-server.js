const express = require('express');
const app = express();

app.use(express.static(__dirname + '/mock'));

// AJAX to /action.
app.post('/action', (req, res, next) => {
  res.send('POST action completed!');
});

// Export the module like this for Brunch.
module.exports = (config, callback) => {
  // Server config is passed within the `config` variable.
  app.listen(config.port, function () {
    console.log(`Example app listening on port ${config.port}!`);
    callback();
  });

  // Return the app; it has the `close()` method, which would be ran when
  // Brunch server is terminated
  return app;
};
