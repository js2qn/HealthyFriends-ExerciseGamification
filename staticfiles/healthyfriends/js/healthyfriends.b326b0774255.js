function setActivePage() { 
    var currentPage;
    currentPage = window.location.pathname;
    if (currentPage == '/polls/' || currentPage.indexOf('vote') > -1) { 
        document.getElementById("poll_nav").classList.add('active');
        document.title = 'Polls'
    }
    else if (currentPage == '/profile/') { 
        document.getElementById("profile_nav").classList.add('active');
        document.title = 'My Profile'
    }
    else if (currentPage == '/fitnesslog/') { 
        document.getElementById("log_nav").classList.add('active');
        document.title = 'My Fitness Log'
    }
    else if (currentPage == '/achievements/') { 
        document.getElementById("achievements_nav").classList.add('active');
        document.title = 'My Achievements'
    }
    else if (currentPage == '/leaderboard/') { 
        document.getElementById("leaderboard_nav").classList.add('active');
        document.title = 'Leaderboard'
    }
    else if (currentPage == '/forum/') { 
        document.getElementById("forum_nav").classList.add('active');
        document.title = 'Forum'
    }
    else if (currentPage == '/guides/') { 
        document.getElementById("guides_nav").classList.add('active');
        document.title = 'Guides'
    }
  }