class GymChatbot {
    constructor() {
        this.responses = {
            greetings: {
                patterns: ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'help'],
                replies: [
                    'Hello! 👋 I\'m your gym assistant. I can help you with:\n\n' +
                    '• Membership information\n' +
                    '• Gym facilities and equipment\n' +
                    '• Personal training\n' +
                    '• Class schedules\n' +
                    '• Operating hours\n\n' +
                    'What would you like to know about?',
                    'Hi there! 😊 Welcome to our gym. I can assist you with membership details, facilities, training, schedules, and more. What interests you?',
                    'Hey! 🌟 I\'m here to help make your fitness journey easier. Ask me about our memberships, facilities, trainers, or classes!'
                ],
                quickReplies: [
                    'Tell me about memberships',
                    'What facilities do you have?',
                    'Personal trainer info',
                    'Class schedule'
                ]
            },
            membership: {
                patterns: ['membership', 'plan', 'package', 'pricing', 'cost', 'fee', 'price', 'join', 'subscribe'],
                replies: [
                    '💪 Our Membership Plans:\n\n' +
                    '🔹 Basic (₹750/month)\n' +
                    '   • Access to gym equipment\n' +
                    '   • Basic fitness assessment\n\n' +
                    '🔹 Premium (₹1,250/month)\n' +
                    '   • All Basic features\n' +
                    '   • Group classes included\n' +
                    '   • Locker access\n\n' +
                    '🔹 Elite (₹2,000/month)\n' +
                    '   • All Premium features\n' +
                    '   • Personal training session\n' +
                    '   • Nutrition consultation\n\n' +
                    'Signup Fee: ₹2,000 (one-time)\n\n' +
                    'Would you like to know more about any specific plan?',
                    '🌟 Ready to start your fitness journey? Here are our plans:\n\n' +
                    '• Basic: ₹750/month - Perfect for beginners\n' +
                    '• Premium: ₹1,250/month - Most popular choice\n' +
                    '• Elite: ₹2,000/month - Complete fitness package\n\n' +
                    'Plus ₹2,000 one-time signup fee\n\n' +
                    'Which plan would you like to learn more about?'
                ],
                quickReplies: [
                    'Basic plan details',
                    'Premium plan details', 
                    'Elite plan details',
                    'Book a tour'
                ]
            },
            facilities: {
                patterns: ['equipment', 'machines', 'facilities', 'amenities', 'gym', 'available', 'what do you have'],
                replies: [
                    '🏋️ Our State-of-the-Art Facilities:\n\n' +
                    '• Cardio Zone\n' +
                    '  - Treadmills\n' +
                    '  - Ellipticals\n' +
                    '  - Bikes\n' +
                    '  - Rowing machines\n\n' +
                    '• Strength Training\n' +
                    '  - Free weights\n' +
                    '  - Weight machines\n' +
                    '  - Smith machines\n\n' +
                    '• Additional Amenities\n' +
                    '  - Locker rooms\n' +
                    '  - Showers\n' +
                    '  - Water stations\n\n' +
                    'Would you like to know more about any specific area?',
                    '🌟 Our gym features modern equipment for all fitness levels:\n\n' +
                    '• Complete cardio section\n' +
                    '• Extensive weight training area\n' +
                    '• Dedicated stretching zone\n' +
                    '• Group fitness studio\n' +
                    '• Clean locker rooms\n\n' +
                    'What would you like to know more about?'
                ],
                quickReplies: [
                    'Cardio equipment',
                    'Weight training',
                    'Amenities',
                    'Book a tour'
                ]
            },
            trainers: {
                patterns: ['trainer', 'personal training', 'instructor', 'coach', 'pt', 'training session'],
                replies: [
                    '👨‍🏫 Personal Training Services:\n\n' +
                    '• Certified Professional Trainers\n' +
                    '• Customized Workout Plans\n' +
                    '• Nutrition Guidance\n' +
                    '• Progress Tracking\n\n' +
                    'Pricing:\n' +
                    '- Single Session: ₹1,000\n' +
                    '- 5 Sessions: ₹4,500\n' +
                    '- 10 Sessions: ₹8,750\n\n' +
                    'Would you like to schedule a free consultation?',
                    '🎯 Our trainers specialize in:\n\n' +
                    '• Weight Loss\n' +
                    '• Muscle Building\n' +
                    '• Sports Training\n' +
                    '• Rehabilitation\n' +
                    '• Senior Fitness\n\n' +
                    'All trainers are certified and experienced. Want to meet one?'
                ],
                quickReplies: [
                    'Trainer profiles',
                    'Training packages',
                    'Book consultation',
                    'Training specialties'
                ]
            },
            schedule: {
                patterns: ['timing', 'hours', 'schedule', 'open', 'close'],
                replies: [
                    '⏰ Our Operating Hours:\n\n' +
                    'Monday - Friday: 5:00 AM - 11:00 PM\n' +
                    'Saturday - Sunday: 6:00 AM - 9:00 PM\n\n' +
                    'We\'re here to fit your schedule!',
                    'We are open Monday to Friday 5:00 AM - 11:00 PM, and weekends 6:00 AM - 9:00 PM.',
                    'Our gym operates all week. Weekdays: 5 AM - 11 PM, Weekends: 6 AM - 9 PM.'
                ],
                quickReplies: [
                    'Class schedule',
                    'Book a tour',
                    'Membership info'
                ]
            },
            classes: {
                patterns: ['class', 'group', 'yoga', 'zumba', 'aerobics', 'sessions'],
                replies: [
                    '🎯 Our Group Classes:\n\n' +
                    'Morning Sessions:\n' +
                    '• 6:00 AM - Yoga\n' +
                    '• 7:30 AM - HIIT\n' +
                    '• 9:00 AM - Zumba\n\n' +
                    'Evening Sessions:\n' +
                    '• 5:00 PM - Spinning\n' +
                    '• 6:30 PM - Body Pump\n' +
                    '• 8:00 PM - Yoga\n\n' +
                    'Would you like to book a class?',
                    '💪 Weekly Class Schedule:\n\n' +
                    'Monday & Wednesday:\n' +
                    '• Yoga\n' +
                    '• HIIT\n' +
                    '• Zumba\n\n' +
                    'Tuesday & Thursday:\n' +
                    '• Spinning\n' +
                    '• Body Pump\n' +
                    '• Pilates\n\n' +
                    'Which class interests you?'
                ],
                quickReplies: [
                    'Class schedule',
                    'Book a class',
                    'Class descriptions',
                    'Instructor info'
                ]
            },
            programs: {
                patterns: ['program', 'workout plan', 'routine', 'fitness plan', 'weight loss', 'muscle gain'],
                replies: [
                    '🎯 Our Fitness Programs:\n\n' +
                    '1. Weight Loss Program\n' +
                    '   • Customized workout plan\n' +
                    '   • Nutrition guidance\n' +
                    '   • Progress tracking\n\n' +
                    '2. Muscle Building\n' +
                    '   • Strength training\n' +
                    '   • Supplement advice\n' +
                    '   • Regular assessments\n\n' +
                    '3. General Fitness\n' +
                    '   • Balanced workouts\n' +
                    '   • Flexibility training\n' +
                    '   • Cardio optimization\n\n' +
                    'Which program interests you?',
                ],
                quickReplies: [
                    'Weight loss program',
                    'Muscle building',
                    'General fitness',
                    'AI Workout Planner'
                ]
            },
            search: {
                patterns: ['search', 'find member', 'lookup', 'member search', 'find someone'],
                replies: [
                    '🔍 You can search for members using:\n\n' +
                    '• Member ID (24-character code)\n' +
                    '• Member name (partial or full)\n' +
                    '• Email address\n\n' +
                    'Use the search feature in the navigation menu to find any member quickly!',
                ],
                quickReplies: [
                    'Go to search',
                    'How to use search',
                    'Member management',
                    'Help with IDs'
                ]
            },
            default: {
                replies: [
                    'I apologize, I didn\'t quite understand that. 😅 Here are some topics I can help with:\n\n' +
                    '• Membership plans\n' +
                    '• Gym facilities\n' +
                    '• Personal training\n' +
                    '• Class schedules\n' +
                    '• Fitness programs\n' +
                    '• Member search\n\n' +
                    'What would you like to know about?',
                    'I\'m not sure about that. 🤔 But I can help you with:\n\n' +
                    '• Membership information\n' +
                    '• Available equipment\n' +
                    '• Training sessions\n' +
                    '• Group classes\n' +
                    '• Operating hours\n' +
                    '• Finding members\n\n' +
                    'Please select a topic!'
                ],
                quickReplies: [
                    'Membership info',
                    'See facilities',
                    'Class schedule',
                    'Search members'
                ]
            }
        };
    }

    // NEW: Smart word boundary matching
    matchesPattern(message, pattern) {
        // Create word boundary regex for exact word matching
        const regex = new RegExp('\\b' + pattern + '\\b', 'i');
        return regex.test(message);
    }

    findMatch(message) {
        const userMessage = message.toLowerCase().trim();
        
        // Check each category
        for (const [category, data] of Object.entries(this.responses)) {
            if (category === 'default') continue;
            
            // Use smart pattern matching instead of includes()
            const matched = data.patterns.some(pattern => {
                return this.matchesPattern(userMessage, pattern);
            });
            
            if (matched) {
                const reply = data.replies[Math.floor(Math.random() * data.replies.length)];
                return {
                    text: reply,
                    quickReplies: data.quickReplies || []
                };
            }
        }
        
        // Default response if no match
        return {
            text: this.responses.default.replies[Math.floor(Math.random() * this.responses.default.replies.length)],
            quickReplies: this.responses.default.quickReplies || []
        };
    }

    respond(message) {
        return this.findMatch(message);
    }
}

// Initialize chatbot
const chatbot = new GymChatbot();

// Handle message sending
function sendMessage() {
    const messageInput = document.getElementById('chat-input');
    const message = messageInput.value.trim();
    
    if (message) {
        // Remove any existing quick replies
        const quickReplies = document.querySelector('.quick-replies');
        if (quickReplies) quickReplies.remove();

        addMessage('user', message);
        const response = chatbot.respond(message);
        setTimeout(() => addMessage('bot', response.text, response.quickReplies), 500);
        messageInput.value = '';
    }
}

// Add message to chat container
function addMessage(sender, message, quickReplies = []) {
    const chatContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    // Convert URLs and newlines to clickable links and line breaks
    const formattedMessage = message
        .replace(/\n/g, '<br>')
        .replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
    
    messageDiv.innerHTML = `<p>${formattedMessage}</p>`;
    chatContainer.appendChild(messageDiv);

    // Add quick replies if available
    if (quickReplies && quickReplies.length > 0 && sender === 'bot') {
        const quickRepliesDiv = document.createElement('div');
        quickRepliesDiv.className = 'quick-replies';
        quickReplies.forEach(reply => {
            const button = document.createElement('button');
            button.className = 'quick-reply-btn';
            button.textContent = reply;
            button.onclick = () => {
                addMessage('user', reply);
                const response = chatbot.respond(reply);
                setTimeout(() => addMessage('bot', response.text, response.quickReplies), 500);
                quickRepliesDiv.remove();
            };
            quickRepliesDiv.appendChild(button);
        });
        chatContainer.appendChild(quickRepliesDiv);
    }

    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Initialize chat with a greeting and UI handlers
document.addEventListener('DOMContentLoaded', function() {
    // Attach UI handlers (toggle, minimize, send, enter key) if elements exist
    const chatToggle = document.querySelector('.chat-toggle');
    const chatWidget = document.querySelector('.chat-widget');
    const minimizeBtn = document.querySelector('.minimize-btn');
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    
    if (chatToggle && chatWidget) {
        chatToggle.addEventListener('click', function() {
            chatWidget.classList.remove('minimized');
            chatToggle.style.display = 'none';
            if (chatInput) chatInput.focus();
        });
    }
    
    if (minimizeBtn && chatWidget) {
        minimizeBtn.addEventListener('click', function() {
            chatWidget.classList.add('minimized');
            if (chatToggle) chatToggle.style.display = 'flex';
        });
    }
    
    if (sendBtn) {
        sendBtn.addEventListener('click', function() {
            sendMessage();
        });
    }
    
    if (chatInput) {
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // Safe: add initial greeting from the bot
    try {
        const initialResponse = chatbot.respond('help');
        addMessage('bot', initialResponse.text, initialResponse.quickReplies);
    } catch (err) {
        console.error('Chatbot init error:', err);
    }
});
