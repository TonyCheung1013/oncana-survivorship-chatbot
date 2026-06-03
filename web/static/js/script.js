document.addEventListener('DOMContentLoaded', () => {
  const collapsibleHeaders = document.querySelectorAll('.collapsible-header');

  collapsibleHeaders.forEach(header => {
    header.addEventListener('click', () => {
      header.classList.toggle('active');
      const content = header.nextElementSibling;
      content.style.display = content.style.display === 'block' ? 'none' : 'block';

      const arrow = header.querySelector('.arrow');
      if (arrow) arrow.classList.toggle('expand');
    });
  });

  loadAllTables();
});

async function loadAllTables() {
  await loadTable('topics', 'topics-table');
  await loadTable('subtopics', 'subtopics-table');
  await loadTable('resource_contents', 'resource-table');
  await loadTable('contacts', 'contacts-table');
  await loadTable('users', 'users-table');
  await loadTable('conversation_logs', 'conversation-logs-table');
  await loadTable('conversation_summaries', 'conversation-summaries-table');
}

async function loadTable(table, tableId) {
  try {
    const res = await fetch(`/api/get_data/${table}`);
    const data = await res.json();
    renderTable(table, tableId, data);
  } catch (err) {
    console.error(`Error loading ${table}:`, err);
  }
}

function renderTable(table, tableId, data) {
  const tableElement = document.getElementById(tableId);
  if (!tableElement) return;

  tableElement.innerHTML = '';

  if (data.length === 0) {
    tableElement.innerHTML = '<tr><td>No data found</td></tr>';
    return;
  }

  const headerRow = document.createElement('tr');
  Object.keys(data[0]).forEach(key => {
    const th = document.createElement('th');
    th.textContent = key;
    headerRow.appendChild(th);
  });
  headerRow.appendChild(document.createElement('th')).textContent = 'Actions';
  tableElement.appendChild(headerRow);

  data.forEach(row => {
    const tr = document.createElement('tr');
    Object.values(row).forEach(val => {
      const td = document.createElement('td');
      td.textContent = val;
      td.classList.add('scrollable-cell');
      tr.appendChild(td);
    });

    const actionTd = document.createElement('td');

    const editBtn = document.createElement('button');
    editBtn.textContent = 'Edit';
    editBtn.addEventListener('click', () => openModal('edit', table, row));

    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Delete';
    deleteBtn.addEventListener('click', () => deleteRow(table, row));

    actionTd.appendChild(editBtn);
    actionTd.appendChild(deleteBtn);
    tr.appendChild(actionTd);

    tableElement.appendChild(tr);
  });
}

function openModal(mode, table, row = {}) {
  const modal = document.getElementById('dataModal');
  const formFields = document.getElementById('formFields');
  formFields.innerHTML = '';

  const fields = mode === 'edit' ? Object.keys(row) : getTableFields(table);

  fields.forEach(key => {
    if (key === 'id' || key === 'message_id' || key === 'conversation_id') return;
    const label = document.createElement('label');
    label.textContent = key;
    const input = document.createElement('input');
    input.type = 'text';
    input.name = key;
    input.value = row[key] || '';
    formFields.appendChild(label);
    formFields.appendChild(input);
  });

  const form = document.getElementById('dataForm');
  form.onsubmit = e => {
    e.preventDefault();
    if (mode === 'edit') updateRow(table, row, form);
    else addRowData(table, form);
  };

  modal.style.display = 'block';
}

function closeModal() {
  document.getElementById('dataModal').style.display = 'none';
}

async function deleteRow(table, row) {
  const id = row.user_id || row.contact_id || row.content_id || row.topic_id || row.subtopic_id || row.message_id || row.conversation_id;
  if (!confirm('Are you sure to delete this record?')) return;
  const res = await fetch(`/api/delete_data/${table}/${id}`, { method: 'DELETE' });
  const result = await res.json();
  if (result.success) loadTable(table, `${table}-table`);
}

async function addRowData(table, form) {
  const data = {};
  [...form.elements].forEach(el => {
    if (el.name) data[el.name] = el.value;
  });
  const res = await fetch(`/api/add_data/${table}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  const result = await res.json();
  if (result.success) {
    loadTable(table, `${table}-table`);
    closeModal();
  } else {
    alert(result.error);
  }
}

async function updateRow(table, row, form) {
  const data = {};
  [...form.elements].forEach(el => {
    if (el.name) data[el.name] = el.value;
  });
  const id = row.user_id || row.contact_id || row.content_id || row.topic_id || row.subtopic_id || row.message_id || row.conversation_id;
  const res = await fetch(`/api/update_data/${table}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  const result = await res.json();
  if (result.success) {
    loadTable(table, `${table}-table`);
    closeModal();
  } else {
    alert(result.error);
  }
}

function getTableFields(table) {
  switch (table) {
    case 'topics':
      return ['topic_id', 'name', 'description', 'keywords'];
    case 'subtopics':
      return ['subtopic_id', 'topic_id', 'name', 'description'];
    case 'resource_contents':
      return ['content_id', 'subtopic_id', 'content_type', 'content_text', 'source_document'];
    case 'contacts':
      return ['contact_id', 'subtopic_id', 'name', 'phone', 'email', 'website'];
    case 'users':
      return ['user_id', 'name', 'password', 'age', 'cancer_type', 'treatment_history'];
    case 'conversation_logs':
      return ['message_id', 'conversation_id', 'user_id', 'timestamp', 'role', 'message_text', 'related_topic_id', 'prompt_used'];
    case 'conversation_summaries':
      return ['conversation_id', 'user_id', 'key_topics', 'key_recommendations', 'contacts_provided', 'summary_text'];
    default:
      return [];
  }
}
