    var btn = $('.with-popup');
    var ddBtn = $('.dd');

    var expanded = false;

    ddBtn.click(function() {
        if (!expanded) {
            $(this).addClass('minus');
        } else {
            $(this).removeClass('minus');
        }

        expanded = !expanded;

        $('.dd-menu', this).slideToggle();
    });

    if (btn.length > 0) {
        function close_popups() {
            $('.popup').css('display', 'none');
        }

        $(document).keyup(function(e) {
            if (e.keyCode === 27)
                close_popups();
        });

        $(document).click(function(e) {
            if ($(e.target).closest(btn).length === 0) {
                close_popups();
            }
        })

        btn.click(function() {
            close_popups();
            $('.popup', this).css('display', 'block');
        });
    }