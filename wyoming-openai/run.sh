#!/usr/bin/with-contenv bashio
# ==============================================================================
# Home Assistant Add-on: Wyoming OpenAI
# Runs Wyoming OpenAI with configuration from add-on options
# ==============================================================================

# Read options
URI=$(bashio::config 'uri')
LOG_LEVEL=$(bashio::config 'log_level')
LANGUAGES=$(bashio::config 'languages')
TTS_OPENAI_URL=$(bashio::config 'tts_openai_url')
TTS_OPENAI_KEY=$(bashio::config 'tts_openai_key')
TTS_MODELS=$(bashio::config 'tts_models')
TTS_VOICES=$(bashio::config 'tts_voices')
TTS_BACKEND=$(bashio::config 'tts_backend')
TTS_PREPROCESSING=$(bashio::config 'tts_preprocessing_enabled')
TTS_REPLACEMENTS=$(bashio::config 'tts_custom_replacements')
STT_OPENAI_URL=$(bashio::config 'stt_openai_url')
STT_OPENAI_KEY=$(bashio::config 'stt_openai_key')
STT_MODELS=$(bashio::config 'stt_models')

bashio::log.info "Starting Wyoming OpenAI..."

# Build command as array (proper quoting)
CMD=(python -m wyoming_openai)

# Required args
CMD+=(--uri "$URI")
CMD+=(--log-level "${LOG_LEVEL^^}")  # Uppercase
CMD+=(--languages $LANGUAGES)

# TTS args
CMD+=(--tts-openai-url "$TTS_OPENAI_URL")
CMD+=(--tts-models $TTS_MODELS)

if bashio::config.has_value 'tts_openai_key'; then
    CMD+=(--tts-openai-key "$TTS_OPENAI_KEY")
fi

if bashio::config.has_value 'tts_voices'; then
    CMD+=(--tts-voices $TTS_VOICES)
fi

if bashio::config.has_value 'tts_backend'; then
    CMD+=(--tts-backend "$TTS_BACKEND")
fi

if bashio::config.has_value 'tts_preprocessing_enabled'; then
    CMD+=(--tts-preprocessing-enabled "$TTS_PREPROCESSING")
fi

if bashio::config.has_value 'tts_custom_replacements'; then
    CMD+=(--tts-custom-replacements "$TTS_REPLACEMENTS")
fi

# STT args (optional)
if bashio::config.has_value 'stt_openai_url'; then
    CMD+=(--stt-openai-url "$STT_OPENAI_URL")
fi

if bashio::config.has_value 'stt_openai_key'; then
    CMD+=(--stt-openai-key "$STT_OPENAI_KEY")
fi

if bashio::config.has_value 'stt_models'; then
    CMD+=(--stt-models $STT_MODELS)
fi

bashio::log.info "Command: ${CMD[*]}"

# Run Wyoming OpenAI
exec "${CMD[@]}"
