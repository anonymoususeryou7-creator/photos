document.addEventListener('DOMContentLoaded', () => {
    const lightbox = document.getElementById('lightbox');
    if (!lightbox) return;

    const lightboxImg = document.getElementById('lightbox-img');
    const closeBtn = document.getElementById('lightbox-close');
    const prevBtn = document.getElementById('lightbox-prev');
    const nextBtn = document.getElementById('lightbox-next');
    const items = Array.from(document.querySelectorAll('.masonry-item'));
    
    // Popup logic
    const welcomePopup = document.getElementById('welcome-popup');
    const welcomeClose = document.getElementById('welcome-close');
    
    if (welcomePopup && welcomeClose) {
        if (!localStorage.getItem('gallery_visited')) {
            welcomePopup.classList.add('active');
        }
        
        welcomeClose.addEventListener('click', () => {
            welcomePopup.classList.remove('active');
            localStorage.setItem('gallery_visited', 'true');
        });
    }

    let currentIndex = -1;

    function openLightbox(index) {
        currentIndex = index;
        const item = items[currentIndex];
        if (!item) return;
        
        const fullSrc = item.getAttribute('data-full-src');
        lightboxImg.src = fullSrc;
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeLightbox() {
        lightbox.classList.remove('active');
        document.body.style.overflow = '';
        setTimeout(() => {
            lightboxImg.src = '';
        }, 300);
    }

    function showNext() {
        if (currentIndex < items.length - 1) {
            openLightbox(currentIndex + 1);
        } else {
            openLightbox(0); // loop
        }
    }

    function showPrev() {
        if (currentIndex > 0) {
            openLightbox(currentIndex - 1);
        } else {
            openLightbox(items.length - 1); // loop
        }
    }

    // Event Listeners
    items.forEach((item, index) => {
        // Only open lightbox if the user didn't click the delete button
        item.addEventListener('click', (e) => {
            if (e.target.closest('.delete-form')) return;
            openLightbox(index);
        });
    });

    closeBtn.addEventListener('click', closeLightbox);
    nextBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        showNext();
    });
    prevBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        showPrev();
    });

    // Close on background click
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox || e.target.classList.contains('lightbox-content')) {
            closeLightbox();
        }
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (!lightbox.classList.contains('active')) return;
        
        if (e.key === 'Escape') closeLightbox();
        if (e.key === 'ArrowRight') showNext();
        if (e.key === 'ArrowLeft') showPrev();
    });

    // Touch swipe navigation for mobile
    let touchStartX = 0;
    let touchStartY = 0;

    lightbox.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].clientX;
        touchStartY = e.changedTouches[0].clientY;
    }, { passive: true });

    lightbox.addEventListener('touchend', (e) => {
        const dx = e.changedTouches[0].clientX - touchStartX;
        const dy = e.changedTouches[0].clientY - touchStartY;

        // Only trigger if horizontal swipe is dominant and long enough
        if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 50) {
            if (dx < 0) showNext();   // swipe left → next
            else showPrev();          // swipe right → previous
        } else if (Math.abs(dy) > 80 && Math.abs(dx) < 40) {
            closeLightbox();          // swipe down → close
        }
    }, { passive: true });
});
