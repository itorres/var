/* Usage
 Create an empty project in https://script.google.com/ and paste the content of this script.
 Program its execution in Resources -> Current project's triggers.
 */
function filterZenDeskMessages() {
    var zenDeskLabelName = 'ZenDesk';
    var zenDeskLabel = GmailApp.getUserLabelByName(zenDeskLabelName);
    if (zenDeskLabel == undefined) {
        zenDeskLabel = GmailApp.createLabel(zenDeskLabelName);
    }
    // Limit the ammount of messages to avoid exceeding the service quotas
    var threads = GmailApp.getInboxThreads(0,5);
    for (var i = 0; i < threads.length; i++) {
        var messages=threads[i].getMessages();
        for (var j = 0; j < messages.length; j++) {
            var message=messages[j];
            var body=message.getRawContent();
            if(body.indexOf("X-Mailer: Zendesk Mailer")>-1){
                zenDeskLabel.addToThread(threads[i]);
                GmailApp.moveThreadToArchive(threads[i]);
            }
        }
    }
}
