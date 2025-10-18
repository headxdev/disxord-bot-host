// CommandSelector.jsx - Frontend für Template-Auswahl
import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

const CommandSelector = () => {
    const [templates, setTemplates] = useState(null);
    const [selectedCategory, setSelectedCategory] = useState('all');
    const [selectedLanguage, setSelectedLanguage] = useState('python');
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedCommand, setSelectedCommand] = useState(null);

    // Animationen
    const containerVariants = {
        hidden: { opacity: 0 },
        visible: { 
            opacity: 1,
            transition: { staggerChildren: 0.1 }
        }
    };

    const itemVariants = {
        hidden: { y: 20, opacity: 0 },
        visible: { 
            y: 0,
            opacity: 1,
            transition: { type: "spring", stiffness: 100 }
        }
    };

    // Lade Templates
    useEffect(() => {
        fetch('/api/templates')
            .then(res => res.json())
            .then(data => setTemplates(data));
    }, []);

    if (!templates) return <div>Loading...</div>;

    const filteredTemplates = templates.templates.filter(template => {
        const matchesCategory = selectedCategory === 'all' || template.category === selectedCategory;
        const matchesSearch = template.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                            template.description.toLowerCase().includes(searchTerm.toLowerCase());
        return matchesCategory && matchesSearch;
    });

    return (
        <div className="min-h-screen bg-gray-900 text-white p-8">
            {/* Header */}
            <header className="mb-8 text-center">
                <h1 className="text-4xl font-bold mb-4">Discord Bot Command Templates</h1>
                <p className="text-gray-400">by headx - the psychon</p>
            </header>

            {/* Controls */}
            <div className="mb-8 flex flex-wrap gap-4 justify-center">
                {/* Kategorie-Filter */}
                <div className="flex gap-2 flex-wrap justify-center">
                    {Object.entries(templates.categories).map(([key, category]) => (
                        <button
                            key={key}
                            onClick={() => setSelectedCategory(key)}
                            className={`px-4 py-2 rounded-full transition-all ${
                                selectedCategory === key 
                                    ? 'bg-blue-600 text-white' 
                                    : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                            }`}
                        >
                            {category.icon} {category.name}
                        </button>
                    ))}
                </div>

                {/* Sprach-Auswahl */}
                <div className="flex gap-2 justify-center">
                    {['python', 'javascript', 'csharp'].map(lang => (
                        <button
                            key={lang}
                            onClick={() => setSelectedLanguage(lang)}
                            className={`px-4 py-2 rounded-full transition-all ${
                                selectedLanguage === lang
                                    ? 'bg-green-600 text-white'
                                    : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                            }`}
                        >
                            {lang.charAt(0).toUpperCase() + lang.slice(1)}
                        </button>
                    ))}
                </div>

                {/* Suche */}
                <input
                    type="text"
                    placeholder="Search commands..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="px-4 py-2 rounded-full bg-gray-800 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-600"
                />
            </div>

            {/* Template Grid */}
            <motion.div 
                className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
                variants={containerVariants}
                initial="hidden"
                animate="visible"
            >
                {filteredTemplates.map(template => (
                    <motion.div
                        key={template.name}
                        variants={itemVariants}
                        className="bg-gray-800 rounded-lg p-6 hover:bg-gray-700 transition-all cursor-pointer"
                        onClick={() => setSelectedCommand(template)}
                    >
                        <div className="flex items-center gap-3 mb-4">
                            <span className="text-2xl">{
                                templates.categories[template.category].icon
                            }</span>
                            <div>
                                <h3 className="font-bold text-xl">{template.name}</h3>
                                <span className="text-sm text-gray-400">
                                    {templates.categories[template.category].name}
                                </span>
                            </div>
                        </div>
                        <p className="text-gray-300 mb-4">{template.description}</p>
                        <div className="flex items-center justify-between">
                            <span className={`px-3 py-1 rounded-full text-sm ${
                                template.complexity === 'Beginner' ? 'bg-green-600' :
                                template.complexity === 'Intermediate' ? 'bg-yellow-600' :
                                'bg-red-600'
                            }`}>
                                {template.complexity}
                            </span>
                            <div className="text-gray-400 text-sm">
                                {template.requires.join(', ')}
                            </div>
                        </div>
                    </motion.div>
                ))}
            </motion.div>

            {/* Command Modal */}
            {selectedCommand && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
                    <div className="bg-gray-800 rounded-lg p-6 max-w-4xl w-full max-h-[90vh] overflow-auto">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-2xl font-bold">{selectedCommand.name}</h2>
                            <button 
                                onClick={() => setSelectedCommand(null)}
                                className="text-gray-400 hover:text-white"
                            >
                                ✕
                            </button>
                        </div>
                        <div className="mb-4">
                            <pre className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
                                <code>
                                    {/* Hier kommt der Code in der ausgewählten Sprache */}
                                    {selectedCommand[selectedLanguage]}
                                </code>
                            </pre>
                        </div>
                        <div className="flex gap-4 mt-4">
                            <button 
                                className="px-4 py-2 bg-blue-600 rounded-lg hover:bg-blue-700 transition-all"
                                onClick={() => {/* Copy to Clipboard */}}
                            >
                                Copy Code
                            </button>
                            <button 
                                className="px-4 py-2 bg-green-600 rounded-lg hover:bg-green-700 transition-all"
                                onClick={() => {/* Install Template */}}
                            >
                                Install Template
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default CommandSelector;
