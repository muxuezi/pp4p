This is a tentative version of PyMailCGI, which ensures
accurate deletions by embedding mail headers text in
message view page as hidden input fields, to be passed 
to safe deletion calls in mailtools package which do
inbox synch tests.  This acounts for rare server inbox 
changes after the mail was fetched, and avoids deleting
wrong emails--the mail displayed is the only one deleted.

This has not been widely tested, may add a few K size
to some pages, and may or may not encounter size limits
in some web browsers/clients.  This seems to work on 
Firefox, after escaping nested '"' quotes, and converting
\r\n from the form field to the \n returned by TOP fetches. 

Search for "#EXPERIMENTAL" to find changes made.  Only 10
lines of code in 3 files were modified: onViewPageAction.py,
onViewListLink.py, and commonhtml.py.

See Chapter 17 for more on this techinique, as well as
more general alternatives that also catch synch errors
on fetches.  This version is tentative, because it is 
incomplete--it addresses only deletions, not inbox
synchronization errors in general.

As is, this really only helps if the mail is deleted 
elsewhere afer it has already been opened for viewing; 
if it is deleted elsewhere before being opened in a view 
window here, the wrong mail will still be fetched from 
the index page, though the mail displayed in the view 
window will be the only one deleted.  Users are expected 
to catch the case where an email other than the one 
selected is fetched, before selecting it for deletion.
