document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#single-view').style.display = 'none';

  // Clear out composition fields
  clear_composition();
}

function clear_composition() {
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#email-view-title').innerHTML = `${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}`;

  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(email_list => {
      const emails = document.querySelector("#emails");

      let html = email_list.map(email => {
        return `
          <li class="email-item card cursor-pointer ${email.read ? 'read' : 'not-read'}" data-id="${email.id}" data-mailbox="${mailbox}">
              <div class="card-body d-flex flex-row justify-content-between align-items-center p-3 ryu-gap pointer-events-none">
                  <div class="d-flex flex-row align-items-center ryu-gap pointer-events-none">
                      <h4 class="h6 m-0 pointer-events-none">${email.sender}</h4>
                      <span class="pointer-events-none">${email.subject}</span>
                  </div>
                  
                  <span class="pointer-events-none">${email.timestamp}</span>
              </div>
          </li>
        `;
      }).join('');

      emails.innerHTML = html;

      emails.querySelectorAll('.email-item').forEach(email => {
        email.addEventListener('click', show_email);
      })
    })
}

function send_email(e) {
  e.preventDefault();

  const recipients = e.target.querySelector("#compose-recipients").value;
  const subject = e.target.querySelector("#compose-subject").value;
  const body = e.target.querySelector("#compose-body").value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients,
      subject,
      body
    })
  })
    .then(response => response.json())
    .then(result => {
      console.log(result);
      load_mailbox('sent');
    })
    .catch(error => {
      console.error("Error:" + error);
    })
}

function show_email(e) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-view').style.display = 'block';

  const id = e.target.dataset.id;
  const mailbox = e.target.dataset.mailbox;

  fetch(`emails/${id}`)
    .then(response => response.json())
    .then(email => {
      let html = `
        <span><strong>From:</strong> ${email.sender}</span><br>
        <span><strong>To:</strong> ${email.recipients.join(', ')}</span><br>
        <span><strong>Subject:</strong> ${email.subject}</span><br>
        <span><strong>Timestamp:</strong> ${email.timestamp}</span><br><br>
        <div class="d-flex flex-row" style="gap:.5rem;">
          <button id="reply" class="btn btn-sm btn-outline-primary">Reply</button>
          ${mailbox !== 'sent' ? `<button id="archive" class="btn btn-sm btn-outline-primary" data-id="${email.id}" data-archived="${email.archived}">${email.archived ? 'Unarchive' : 'Archive'}</button>` : ''}
        </div>
        <hr>
        <pre style="font-family:inherit;">${email.body}</pre>
      `;

      console.log(email.body)

      document.querySelector('#single-view').innerHTML = html;

      if (mailbox !== 'sent') document.querySelector('#archive').addEventListener('click', toggle_archive);

      document.querySelector('#reply').addEventListener('click', () => {
        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'block';
        document.querySelector('#single-view').style.display = 'none';

        document.querySelector('#compose-recipients').value = email.sender;
        document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
        document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:\n${email.body}`;
      });
    })
    .catch(error => console.log(error));

  fetch(`emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
}

function toggle_archive(e) {
  const id = e.target.dataset.id;
  const archived = !(e.target.dataset.archived === 'true');

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({ archived })
  }).then(() => {
    load_mailbox('inbox')
  })
}