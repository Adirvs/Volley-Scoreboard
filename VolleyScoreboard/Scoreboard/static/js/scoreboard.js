document.addEventListener('DOMContentLoaded', () => {
  const board = document.querySelector('.scoreboard-wrapper');
  if (!board) return;

  const scoreA = document.getElementById('score-a');
  const scoreB = document.getElementById('score-b');
  const setsA = document.getElementById('sets-a');
  const setsB = document.getElementById('sets-b');
  const serveA = document.getElementById('serve-a');
  const serveB = document.getElementById('serve-b');
  const currentSet = document.getElementById('current-set');
  const matchStatus = document.getElementById('match-status');
  const actionError = document.getElementById('action-error');

  const btnAddA = document.getElementById('btn-add-a');
  const btnSubA = document.getElementById('btn-sub-a');
  const btnAddB = document.getElementById('btn-add-b');
  const btnSubB = document.getElementById('btn-sub-b');
  const btnReset = document.getElementById('btn-reset');
  const btnNextSet = document.getElementById('btn-next-set');

  function animateScore(element) {
    if (!element) return;
    element.classList.remove('score-pop');
    void element.offsetWidth;
    element.classList.add('score-pop');
  }

  function showError(message) {
    actionError.textContent = message;
    actionError.hidden = false;
  }

  async function sendScoreAction(actionUrl) {
    actionError.hidden = true;
    try {
      const csrfToken = getCookie('csrftoken');
      if (!csrfToken) throw new Error('Token CSRF não encontrado. Atualize a página e tente novamente.');

      const response = await fetch(actionUrl, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'Accept': 'application/json'
        }
      });
      const data = await response.json();

      if (!response.ok) {
        if (data.code === 'match_unavailable') {
          window.location.assign(board.dataset.setupUrl);
          return;
        }
        throw new Error(data.error || `Erro na requisição (${response.status}).`);
      }

      updateUI(data);
      if (data.changed_team === 'A') animateScore(scoreA);
      if (data.changed_team === 'B') animateScore(scoreB);
    } catch (error) {
      console.error('Falha ao atualizar o placar:', error);
      showError(error.message || 'Falha na comunicação com o servidor.');
    }
  }

  function updateUI(data) {
    if (data.score_a !== undefined) scoreA.textContent = data.score_a;
    if (data.score_b !== undefined) scoreB.textContent = data.score_b;
    if (data.sets_a !== undefined) setsA.textContent = data.sets_a;
    if (data.sets_b !== undefined) setsB.textContent = data.sets_b;
    if (data.current_set !== undefined) currentSet.textContent = `Set Atual (Set ${data.current_set})`;

    if (data.current_server) {
      serveA.classList.toggle('active', data.current_server === 'A');
      serveB.classList.toggle('active', data.current_server === 'B');
    }

    const canPlay = !data.set_finished && !data.is_finished;
    [btnAddA, btnSubA, btnAddB, btnSubB].forEach((button) => {
      if (button) button.disabled = !canPlay;
    });
    if (btnSubA) btnSubA.disabled = !canPlay || !data.can_undo_a;
    if (btnSubB) btnSubB.disabled = !canPlay || !data.can_undo_b;
    if (btnReset) btnReset.disabled = !canPlay;
    if (btnNextSet) btnNextSet.hidden = !data.set_finished || data.is_finished;

    if (data.is_finished) {
      matchStatus.textContent = `Partida encerrada: Time ${data.match_winner} venceu.`;
    } else if (data.set_finished) {
      matchStatus.textContent = `Time ${data.set_winner} venceu o set.`;
    } else {
      matchStatus.textContent = `Set ${data.current_set} em andamento.`;
    }
  }

  function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split(';') : [];
    for (const cookie of cookies) {
      const trimmedCookie = cookie.trim();
      if (trimmedCookie.startsWith(`${name}=`)) {
        return decodeURIComponent(trimmedCookie.substring(name.length + 1));
      }
    }
    return null;
  }

  if (btnAddA) btnAddA.addEventListener('click', () => sendScoreAction(board.dataset.pointAUrl));
  if (btnSubA) btnSubA.addEventListener('click', () => sendScoreAction(board.dataset.undoAUrl));
  if (btnAddB) btnAddB.addEventListener('click', () => sendScoreAction(board.dataset.pointBUrl));
  if (btnSubB) btnSubB.addEventListener('click', () => sendScoreAction(board.dataset.undoBUrl));

  if (btnReset) {
    btnReset.addEventListener('click', () => {
      if (confirm('Deseja realmente reiniciar o set atual?')) {
        sendScoreAction(board.dataset.resetUrl);
      }
    });
  }

  if (btnNextSet) {
    btnNextSet.addEventListener('click', () => sendScoreAction(board.dataset.nextSetUrl));
  }

  document.addEventListener('keydown', (event) => {
    if (['INPUT', 'SELECT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;

    switch (event.key.toLowerCase()) {
      case 'a':
      case 'arrowleft':
        if (btnAddA) btnAddA.click();
        break;
      case 'z':
        if (btnSubA) btnSubA.click();
        break;
      case 'l':
      case 'arrowright':
        if (btnAddB) btnAddB.click();
        break;
      case 'm':
        if (btnSubB) btnSubB.click();
        break;
    }
  });
});
