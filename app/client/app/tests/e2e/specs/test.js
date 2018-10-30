// For authoring Nightwatch tests, see
// http://nightwatchjs.org/guide#usage
var localhost = 'http://localhost:8080'
module.exports = {
  'default page': browser => {
    browser
      .url(localhost)
      .waitForElementVisible('h2', 3000)
      .assert.containsText('h2', 'Sending an email via APIs')
      .setValue('input[name=emailto]', 'foretribe@gmail.com')
      .setValue('input[name=emailtitle]', 'Test email')
      .setValue('textarea', 'Input area test')
      .click('button[name=submit]')
      .pause(3000)
      .assert.containsText('span', 'send email error')
      .end()
  }
}
