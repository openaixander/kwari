 // Header scroll effect
        const navbar = document.querySelector('.navbar-custom');
        let lastScroll = 0;
        
        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;
            if (currentScroll > 60) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
            lastScroll = currentScroll;
        });
        
        // Category filter functionality
        const filterButtons = document.querySelectorAll('.filter-btn');
        
        filterButtons.forEach(button => {
            button.addEventListener('click', function() {
                filterButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                // Show loading overlay briefly
                const loadingOverlay = document.getElementById('loadingOverlay');
                loadingOverlay.classList.add('active');
                
                setTimeout(() => {
                    loadingOverlay.classList.remove('active');
                }, 400);
            });
        });
        
        // Sort functionality
        const sortSelect = document.getElementById('sortSelect');
        
        sortSelect.addEventListener('change', function() {
            const loadingOverlay = document.getElementById('loadingOverlay');
            loadingOverlay.classList.add('active');
            
            setTimeout(() => {
                loadingOverlay.classList.remove('active');
            }, 400);
        });
        
        // Add to cart buttons
        const addToCartButtons = document.querySelectorAll('.btn-add-cart');
        
        addToCartButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.stopPropagation();
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="bi bi-check2"></i> Added';
                this.style.backgroundColor = '#22c55e';
                
                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.style.backgroundColor = '';
                }, 1500);
            });
        });
        
        // Load More functionality
        const loadMoreBtn = document.querySelector('.load-more-btn');
        
        loadMoreBtn.addEventListener('click', function() {
            const loadingOverlay = document.getElementById('loadingOverlay');
            loadingOverlay.classList.add('active');
            
            setTimeout(() => {
                loadingOverlay.classList.remove('active');
                this.textContent = 'All Products Loaded';
                this.disabled = true;
                this.style.opacity = '0.6';
            }, 800);
        });