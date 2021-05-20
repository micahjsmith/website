Title: The poor man's Google Sheets mail merge
Date: 2020-12-01
Modified: 2021-05-20
Category: life
Tags: gsuite, email, scripting
Slug: poor-mans-google-sheets-mail-merge
Authors: Micah Smith

If you're not in a corporate environment, you're probably not sending many [*mail merges*](https://en.wikipedia.org/wiki/Mail_merge) in which you automatically send many emails to different recipients with customized content for each recipient. I recently had to send about 150 emails during my work for a student organization I am involved in. Content in the message body had to be customized for each recipient, so we couldn't use other simple mass mailing techniques like the bcc trick or creating a custom email list.

At an enterprise, you'd probably use Excel/Outlook to achieve this using built-in mail merge functionality. Using Google Sheets, this is not so easy.

The [official solution](https://developers.google.com/gsuite/solutions/mail-merge) is to use Google Apps Script and Gmail Message Templates. This requires you to both to be using the Gmail client and to authorize a script someone else wrote and muck around with developer permissions. It's usually a good thing to reuse reliable code written by others! However, in some cases you may want a more lightweight solution that is more flexible.

In this tutorial I show you a neat solution that just relies upon a simple Google Sheet, mailto links, and keyboard shortcuts. Using this, I was able to do a "manual" mail merge in about 5 minutes of idle clicking.

### Mail merge scenario

Suppose that you have a "dataset" (sheet) of names and ages. You want to send a customized email to each person in your dataset letting them know their own age. You organize your data in a sheet without thinking at all about how you will send the emails. Preparing the emails will be done in a separate sheet.

<img title="Data sheet" alt="Data sheet with email address, name, and age" src="{static}/images/poor-mans-mail-merge/poor-mans-mail-merge-00.png" style="border: 1px solid black" width="30%" />

### Create the message content

Create a separate sheet in which you will prepare the email messages. For columns, you will have the recipient of your email and other headers such as cc, bcc, subject, and body.

Fill these columns in, possibly using formulas to merge data from your first sheet into the text.

For example, to create the message body, we use this formula:

```text
="Hello " & Data!B2 & ",
You are " & Data!C2 & " years old.
Bye!"
```

You should compose the body in a separate text editor for a better composition experience, and substitute in placeholders for formulas when you transfer it to the spreadsheet.

You will be left with something like this:

<img title="Mail merge sheet" alt="Mail merge sheet after creating message content" src="{static}/images/poor-mans-mail-merge/poor-mans-mail-merge-01.png" style="border: 1px solid black" />


### Create the mailto link

Use a formula to create a mailto link from the message content[^1].

[Mailto links](https://en.wikipedia.org/wiki/Mailto) are URLs of the form `mailto:` that allow you to request an email message to be prepared with different parameters, such as the recipient, the subject line, and the body. These are mostly used just to turn your contact address into a link that opens in someone's email client, but can be much more useful. You can even specify arbitrary email headers (spec at [RFC 6068](https://tools.ietf.org/html/rfc6068)).

```text
=HYPERLINK(
    "mailto:" & A2
    & "?"
    & JOIN(
        "&",
        $B$1 & "=" & ENCODEURL(B2),
        $C$1 & "=" & ENCODEURL(C2),
        $D$1 & "=" & ENCODEURL(D2),
        $E$1 & "=" & ENCODEURL(E2),
    ),
    "send"
)
```

This will create a link that looks like this:

```text
mailto:foo@example.com?cc=&bcc=qux%40test.org&subject=Your%20age&body=Hello%20Foo%2C%0AYou%20are%2038%20years%20old.%0ABye%21&
```

[Try me to see how this looks in your own email client!](mailto:foo@example.com?cc=&bcc=qux%40test.org&subject=Your%20age&body=Hello%20Foo%2C%0AYou%20are%2038%20years%20old.%0ABye%21&)

Your email client should show you a prepared message with the To, Bcc, Subject, and Body fields already filled out (in the case of this URL). You will now send the email right away without further modification.

<img src="{static}/images/poor-mans-mail-merge/poor-mans-mail-merge-sample-email.png" width="30%" />

Some notes:

- most email clients will also insert your email signature if you have one configured
- the fields are all URL-encoded using `ENCODEURL` so that they will render correctly in the prepared message
- to send an email to multiple recipients, you can include the addresses within the single cell separated by commas.
- it's okay to leave any of the cells blank, such as the cc or bcc fields, `&cc=` is allowed by the spec.
- the formula has a trailing `&` but this is allowed by the spec.

<img title="Mail merge sheet" alt="Mail merge sheet after creating mailto link" src="{static}/images/poor-mans-mail-merge/poor-mans-mail-merge-02.png" style="border: 1px solid black" />

### Send emails in a batch

Select a group of 5-10 cells in the "Link" column. Then use a keyboard shortcut [^2] to click the hyperlink, such as <kbd>Option</kbd> <kbd>Enter</kbd>. Depending on your mail client, this will open *n* windows, with the prepared message ready to send in each of them. You can rapidly use keyboard shortcuts to send them, such as <kbd>Command</kbd> <kbd>Enter</kbd> for either AirMail or Gmail.

When the emails in a batch have successfully been sent, mark them in the sheet accordingly.

### Rich text formatting

Note that rich text formatting (font size, font style, hyperlinks) will not transfer to a Sheets cell if you copy-and-paste. Instead, you should try to export your document to HTML and then copy the raw HTML into a cell. In most email clients, they will correctly interpret a mailto link that has encoded HTML by converting the content back into rich text in the email editor and setting the content type header to `text/html` appropriately.

One detail is that Sheets does not allow the `"` character to appear in the middle of a string in a formula nor is it possible to escape it. If you can, just substitute the `'` character. If you must use the double quote, the best solution is to concatenate the formula `CHAR(34)` (which encodes a double quote) in the middle of a string.

#### Example

Let's say you are trying to include both HTML markup and a double quote in a formula cell to use in a mailto link.

Cell input

```text
="According to Wikipedia, <a class='font-style: italic;'
href='https://en.wikipedia.org/wiki/Oncideres_mirador'>Oncideres mirador</a> is
" & CHAR(34) & "a species of beetle in the family Cerambycidae" & CHAR(34) &
"."
```

Cell output

```html
According to Wikipedia, <a class='font-style: italic;'
href='https://en.wikipedia.org/wiki/Oncideres_mirador'>Oncideres mirador</a> is
"a species of beetle in the family Cerambycidae".
```

HTML output

> According to Wikipedia, [*Oncideres mirador*](https://en.wikipedia.org/wiki/Oncideres_mirador) is "a species of beetle in the family Cerambycidae".

Of course, you don't have to do anything crazy like this if you are not using formulas in the cell. You can just paste the HTML in directly.

### A note on Gmail

If you want to use the Gmail web application as your mail client, then you need to configure your browser appropriately. Chrome was easiest to configure for me, even though I prefer Firefox for almost everything. See [here](https://wiki.carleton.edu/display/itskb/Configuring+Mailto+links+to+use+Gmail).

If you use Gmail, then you will have *n* tabs in your browser window. You can tab through them in order with <kbd>Control</kbd> <kbd>Tab</kbd>. On each tab, use the keyboard shortcut to send the message and immediately navigate to the next tab while the message is sending. The behavior of Gmail's standalone compose window is that if the message sends successfully, the tab will close itself. So if all of your messages send successfully, you will be left with a single tab, which is your spreadsheet. You can then continue with the next batch.

### Conclusion

That's it! This setup requires no scripting or use of developer tools and you can use any email client. It's a reasonable approach if you are sending 10 – 500 emails that need to be customized.

You can also check out [this demo spreadsheet](https://docs.google.com/spreadsheets/d/1jSSIMBfyAZYgrtlg-9_E8W0ZDm2Py98SdqauKUaD-qY/edit?usp=sharing).

Let me know in the comments if you find this helpful or have any improvements on this approach.

[^1]: There may be better ways to create this formula that doesn't require adding separate lines for each header, maybe using [`ARRAYFORMULA`](https://support.google.com/docs/answer/3093275?hl=en) or something beyond my Google Sheets expertise. Let me know in the comments if you figure this out.

[^2]: I'll refer to various keyboard shortcuts, which reflects my setup of macOS. Please substitute the relevant keyboard shortcuts for your own setup.
