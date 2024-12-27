from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from common.definitions import DB_MODEL_SETTINGS as DBS, UI_SETTINGS, AI_MODEL_SETTINGS

Base = declarative_base()


class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(DBS['string_field_lengths']['title']), nullable=False)
    icon = Column(String(DBS['string_field_lengths']['icon']), nullable=False)
    content = Column(Text, nullable=False)
    actions = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ChatMessage(Base):
    __tablename__ = 'chat_messages'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    role = Column(String(DBS['string_field_lengths']['role']), nullable=False)  # 'user', 'aime', 'admin'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


class HistoryItem(Base):
    __tablename__ = 'history_items'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(DBS['string_field_lengths']['title']), nullable=False)
    content_type = Column(String(DBS['string_field_lengths']['content_type']), nullable=False)
    content = Column(JSON, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


class UserSettings(Base):
    __tablename__ = 'user_settings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    theme = Column(String(DBS['string_field_lengths']['theme']), nullable=False, default=UI_SETTINGS['theme']['default'])
    layout = Column(String(DBS['string_field_lengths']['layout']), nullable=False, default=UI_SETTINGS['layout']['default'])
    ai_model = Column(String(DBS['string_field_lengths']['ai_model']), nullable=False, default=AI_MODEL_SETTINGS['default_model'])
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
