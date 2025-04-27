#!/usr/bin/env python3
# prepare_rds_data.py
import os
import sys
import subprocess
import warnings
import numpy as np
import pandas as pd
from pathlib import Path
import pyreadr
import json

# --- Конфигурация ---
# Базовые пути
BASE_DIR = Path("ai_scientist")
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = Path("prepared_data")

# RDS файлы
RDS_FILES = {
    "classified": DATA_DIR / "wl_df_bca_classified.rds",
    "volume": DATA_DIR / "wl_df_bca_final_volume.rds",
}

# Имена объектов внутри RDS файлов (None если не известно)
RDS_OBJECT_NAMES = {
    "classified": None,
    "volume": None,
}

# Колонка для объединения
MERGE_COLUMN = 'patient_id'

# Ключевые колонки и их описания
VARIABLE_DEFINITIONS = {
    # Временные переменные
    'surv_time_months': 'Время наблюдения в месяцах',
    'surv_status': 'Статус выживания (1=событие, 0=цензурирование)',
    
    # MELD параметры
    'meld_score': 'Общий MELD score',
    'lab_meld': 'Лабораторный MELD score',
    
    # Демографические параметры
    'age': 'Возраст пациента',
    'sex': 'Пол пациента (M/F)',
    
    # Параметры состава тела
    'low_AMVI': 'Низкий Abdominal Muscle Volume Index (<2139.32 cm³/m²)',
    'high_IMAC': 'Высокий Intramuscular Adipose Content (≥0.147)',
    'high_VSR': 'Высокий Visceral-to-Subcutaneous Ratio (≥0.393)',
    
    # Дополнительные параметры
    'EAT_Index': 'Epicardial Adipose Tissue Index',
    'PAT_Index': 'Periaortic Adipose Tissue Index',
}

# Требуемые колонки
REQUIRED_COLS = list(VARIABLE_DEFINITIONS.keys())

# Выходные файлы
OUTPUT_FILES = {
    'data': OUTPUT_DIR / "prepared_experiment_data.parquet",
    'metadata': OUTPUT_DIR / "data_metadata.json",
    'analysis_ready': OUTPUT_DIR / "analysis_ready_data.parquet"
}

# --- Конец Конфигурации ---

def setup_logging():
    """Настройка логирования"""
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

def install_package(package, logger):
    """Установка пакета Python"""
    logger.info(f"Устанавливаем {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        logger.info(f"{package} успешно установлен")
    except subprocess.CalledProcessError as e:
        logger.error(f"Ошибка при установке {package}: {e}")
        sys.exit(1)

def check_dependencies(logger):
    """Проверка и установка зависимостей"""
    required_packages = ['pyreadr', 'fastparquet', 'lifelines', 'scikit-learn']
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            install_package(package, logger)

def load_rds_file(file_path, object_name, logger):
    """Загрузка RDS файла"""
    if not file_path.exists():
        logger.error(f"Файл не найден: {file_path}")
        sys.exit(1)
        
    logger.info(f"Загрузка RDS файла: {file_path}")
    try:
        rds_data = pyreadr.read_r(str(file_path))
        
        # Определение DataFrame
        if object_name and object_name in rds_data:
            df = rds_data[object_name]
        elif len(rds_data) == 1:
            df = rds_data[list(rds_data.keys())[0]]
            logger.info(f"  Найден один объект: {list(rds_data.keys())[0]}")
        else:
            logger.error(f"Не удалось однозначно определить DataFrame в {file_path}")
            logger.error(f"Доступные объекты: {list(rds_data.keys())}")
            sys.exit(1)
            
        logger.info(f"  Загружен DataFrame формы: {df.shape}")
        return df
        
    except Exception as e:
        logger.error(f"Ошибка при загрузке {file_path}: {e}")
        sys.exit(1)

def process_dataframes(dataframes, logger):
    """Обработка и объединение DataFrame"""
    logger.info("Обработка и объединение данных...")
    
    if "classified" in dataframes and "volume" in dataframes:
        # Объединение данных
        df_final = pd.merge(
            dataframes["classified"],
            dataframes["volume"],
            on=MERGE_COLUMN,
            how='inner'
        )
        logger.info(f"  Объединенный DataFrame формы: {df_final.shape}")
    elif "classified" in dataframes:
        df_final = dataframes["classified"]
        logger.info("  Используем только 'classified' DataFrame")
    else:
        logger.error("Недостаточно данных для обработки")
        sys.exit(1)
    
    return df_final

def validate_dataframe(df, logger):
    """Проверка DataFrame на наличие необходимых колонок"""
    missing_cols = [col for col in REQUIRED_COLS if col not in df.columns]
    if missing_cols:
        logger.warning(f"Отсутствующие колонки: {missing_cols}")
        logger.warning("Это может повлиять на работу агента")
        
    # Проверка типов данных
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    logger.info(f"Числовые колонки: {list(numeric_cols)}")
    
    # Проверка пропущенных значений
    na_counts = df.isna().sum()
    if na_counts.any():
        logger.warning("Найдены пропущенные значения:")
        logger.warning(na_counts[na_counts > 0])
    
    return df

def prepare_analysis_data(df, logger):
    """Подготовка данных для анализа"""
    logger.info("Подготовка данных для анализа...")
    
    # Создание копии для анализа
    df_analysis = df.copy()
    
    # Добавление категориальных переменных для MELD
    df_analysis['meld_group'] = pd.cut(
        df_analysis['meld_score'],
        bins=[-np.inf, 15, np.inf],
        labels=['low', 'high']
    )
    
    # Подготовка категориальных переменных
    categorical_cols = ['sex', 'meld_group']
    for col in categorical_cols:
        if col in df_analysis.columns:
            df_analysis[col] = df_analysis[col].astype('category')
    
    # Проверка и преобразование временных переменных
    if 'surv_time_months' in df_analysis.columns:
        df_analysis['surv_time_months'] = pd.to_numeric(df_analysis['surv_time_months'], errors='coerce')
    
    if 'surv_status' in df_analysis.columns:
        df_analysis['surv_status'] = pd.to_numeric(df_analysis['surv_status'], errors='coerce')
    
    return df_analysis

def save_metadata(df, output_file, logger):
    """Сохранение метаданных о данных"""
    logger.info("Сохранение метаданных...")
    
    metadata = {
        'variable_definitions': VARIABLE_DEFINITIONS,
        'data_summary': {
            'n_patients': len(df),
            'n_events': int(df['surv_status'].sum()) if 'surv_status' in df.columns else None,
            'median_followup': float(df['surv_time_months'].median()) if 'surv_time_months' in df.columns else None,
        },
        'column_info': {
            col: {
                'type': str(df[col].dtype),
                'missing_values': int(df[col].isna().sum()),
                'unique_values': int(df[col].nunique()) if df[col].dtype == 'object' else None,
            }
            for col in df.columns
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Метаданные сохранены в: {output_file}")

def main():
    # Настройка логирования
    logger = setup_logging()
    logger.info("Начало подготовки данных")
    
    # Проверка зависимостей
    check_dependencies(logger)
    
    # Создание выходной директории
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    try:
        # Загрузка RDS файлов
        dataframes = {}
        for key, path in RDS_FILES.items():
            df = load_rds_file(path, RDS_OBJECT_NAMES.get(key), logger)
            dataframes[key] = df
        
        # Обработка данных
        df_final = process_dataframes(dataframes, logger)
        
        # Валидация данных
        df_final = validate_dataframe(df_final, logger)
        
        # Подготовка данных для анализа
        df_analysis = prepare_analysis_data(df_final, logger)
        
        # Сохранение данных
        logger.info(f"Сохранение данных в: {OUTPUT_FILES['data']}")
        df_final.to_parquet(OUTPUT_FILES['data'], index=False, engine='fastparquet')
        
        # Сохранение данных для анализа
        logger.info(f"Сохранение данных для анализа в: {OUTPUT_FILES['analysis_ready']}")
        df_analysis.to_parquet(OUTPUT_FILES['analysis_ready'], index=False, engine='fastparquet')
        
        # Сохранение метаданных
        save_metadata(df_final, OUTPUT_FILES['metadata'], logger)
        
        logger.info("Данные успешно сохранены")
        
        # Вывод инструкций
        print("\n--- Что делать дальше ---")
        print(f"1. Подготовленные данные сохранены в:")
        print(f"   - Основные данные: {OUTPUT_FILES['data']}")
        print(f"   - Данные для анализа: {OUTPUT_FILES['analysis_ready']}")
        print(f"   - Метаданные: {OUTPUT_FILES['metadata']}")
        print("\n2. Для анализа данных используйте:")
        print("   - Cox regression: lifelines.CoxPHFitter")
        print("   - ROC анализ: sklearn.metrics.roc_curve, roc_auc_score")
        print("   - Kaplan-Meier: lifelines.KaplanMeierFitter")
        print("   - Стратифицированный анализ: lifelines.StratifiedKFold")
        
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main() 