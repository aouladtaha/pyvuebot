// Access to the Telegram WebApp instance
const tg = window.Telegram?.WebApp;

// Utility functions for Telegram Mini App
export default {
  // Initialize Telegram Mini App
  init() {
    if (tg) {
      tg.ready();
      tg.expand();
    }
  },

  // Get user data from Telegram
  getUserData() {
    // For development/testing without Telegram
    if (!tg || !tg.initDataUnsafe?.user) {
      // Check if we have a dev user ID stored
      const devUserId =
        localStorage.getItem("telegram-dev-user-id") ||
        Math.floor(Math.random() * 10000);

      return {
        id: parseInt(devUserId),
        first_name: "Guest",
        username: "guest_" + devUserId,
        isGuest: true,
      };
    }

    const user = tg.initDataUnsafe.user;
    return {
      id: user.id,
      first_name: user.first_name,
      last_name: user.last_name,
      username: user.username,
      language_code: user.language_code,
      isGuest: false,
    };
  },

  // Close the mini app
  close() {
    if (tg) {
      tg.close();
    } else {
      // For development
      window.close();
    }
  },

  // Show the main button
  showMainButton(text, callback) {
    if (!tg) return;

    tg.MainButton.setText(text);
    tg.MainButton.show();
    tg.MainButton.onClick(callback);
  },

  // Hide the main button
  hideMainButton() {
    if (tg) {
      tg.MainButton.hide();
    }
  },
};
