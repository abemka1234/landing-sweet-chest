document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.feedbacks');
    const prevBtn = document.querySelectorAll('.feedbacks-button')[0];
    const nextBtn = document.querySelectorAll('.feedbacks-button')[1];
    
    // Функция для удаления приставки small у всех внутренних элементов
    function removeSmallPrefix(element) {
        if (!element) return;
        
        // Проходим по всем дочерним элементам
        const allElements = element.querySelectorAll('*');
        allElements.forEach(el => {
            // Получаем все классы элемента
            const classes = Array.from(el.classList);
            classes.forEach(className => {
                if (className.includes('-small')) {
                    // Убираем -small из названия класса
                    const newClassName = className.replace('-small', '');
                    el.classList.remove(className);
                    el.classList.add(newClassName);
                }
            });
        });
    }
    
    // Функция для добавления приставки small
    function addSmallPrefix(element) {
        if (!element) return;
        
        const allElements = element.querySelectorAll('*');
        allElements.forEach(el => {
            const classes = Array.from(el.classList);
            classes.forEach(className => {
                if (!className.includes('-small') && className !== 'feedback' && className !== 'feedback-left' && className !== 'feedback-right') {
                    const newClassName = className + '-small';
                    el.classList.remove(className);
                    el.classList.add(newClassName);
                }
            });
        });
    }
    
    // Функция для сдвига вправо
    function shiftRight() {
        // Получаем все карточки
        const cards = Array.from(container.children);
        
        // Убираем small у центральной карточки, если она есть
        const centerCard = cards.find(card => card.classList.contains('feedback'));
        if (centerCard) {
            removeSmallPrefix(centerCard);
        }
        
        // Добавляем small крайним карточкам
        const leftCard = cards.find(card => card.classList.contains('feedback-left'));
        const rightCard = cards.find(card => card.classList.contains('feedback-right'));
        
        if (leftCard) addSmallPrefix(leftCard);
        if (rightCard) addSmallPrefix(rightCard);
        
        // Меняем классы местами (сдвиг вправо)
        // feedback-left -> feedback
        // feedback -> feedback-right
        // feedback-right -> feedback-left
        
        const newClasses = [];
        cards.forEach(card => {
            if (card.classList.contains('feedback-left')) {
                card.classList.remove('feedback-left');
                card.classList.remove('feedback-small')
                card.classList.add('feedback');
                newClasses.push('feedback');
            } else if (card.classList.contains('feedback')) {
                card.classList.remove('feedback');
                card.classList.add('feedback-small')
                card.classList.add('feedback-right');
                newClasses.push('feedback-right');
            } else if (card.classList.contains('feedback-right')) {
                card.classList.remove('feedback-right');
                card.classList.add('feedback-left');
                newClasses.push('feedback-left');
            }
        });
        
        // Обновляем small приставки
        setTimeout(() => {
            const newCenterCard = container.querySelector('.feedback');
            if (newCenterCard) {
                removeSmallPrefix(newCenterCard);
            }
            
            const newLeftCard = container.querySelector('.feedback-left');
            const newRightCard = container.querySelector('.feedback-right');
            
            if (newLeftCard) addSmallPrefix(newLeftCard);
            if (newRightCard) addSmallPrefix(newRightCard);
        }, 10);
    }
    
    // Функция для сдвига влево
    function shiftLeft() {
        const cards = Array.from(container.children);
        
        // Убираем small у центральной карточки
        const centerCard = cards.find(card => card.classList.contains('feedback'));
        if (centerCard) {
            removeSmallPrefix(centerCard);
        }
        
        // Добавляем small крайним карточкам
        const leftCard = cards.find(card => card.classList.contains('feedback-left'));
        const rightCard = cards.find(card => card.classList.contains('feedback-right'));
        
        if (leftCard) addSmallPrefix(leftCard);
        if (rightCard) addSmallPrefix(rightCard);
        
        // Меняем классы местами (сдвиг влево)
        const newClasses = [];
        cards.forEach(card => {
            if (card.classList.contains('feedback-left')) {
                card.classList.remove('feedback-left');
                card.classList.add('feedback-right');
                newClasses.push('feedback-right');
            } else if (card.classList.contains('feedback')) {
                card.classList.remove('feedback');
                card.classList.add('feedback-small')
                card.classList.add('feedback-left');
                
                newClasses.push('feedback-left');
            } else if (card.classList.contains('feedback-right')) {
                card.classList.remove('feedback-right');
                card.classList.add('feedback');
                card.classList.remove('feedback-small')
                newClasses.push('feedback');
            }
        });
        
        // Обновляем small приставки
        setTimeout(() => {
            const newCenterCard = container.querySelector('.feedback');
            if (newCenterCard) {
                removeSmallPrefix(newCenterCard);
            }
            
            const newLeftCard = container.querySelector('.feedback-left');
            const newRightCard = container.querySelector('.feedback-right');
            
            if (newLeftCard) addSmallPrefix(newLeftCard);
            if (newRightCard) addSmallPrefix(newRightCard);
        }, 10);
    }
    
    // Навешиваем обработчики на кнопки
    if (prevBtn) {
        prevBtn.addEventListener('click', shiftLeft);
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', shiftRight);
    }
});