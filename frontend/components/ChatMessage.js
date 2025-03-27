import { motion } from 'framer-motion';

export default function ChatMessage({ text, type }) {
  const isUser = type === 'user';

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      style={{
        display: 'flex',
        justifyContent: isUser ? 'flex-end' : 'flex-start'
      }}
    >
      <div style={{
        background: isUser ? '#4A44D6' : '#e5e7eb',
        padding: '10px 15px',
        borderRadius: '18px',
        maxWidth: '75%',
        wordWrap: 'break-word',
        color: '#000',
        whiteSpace: 'pre-line'
      }}>
        {text}
      </div>
    </motion.div>
  );
}
