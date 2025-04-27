#!/usr/bin/env python3
# analyze_bc_meld.py
import os
import sys
import json
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from lifelines import CoxPHFitter, KaplanMeierFitter
from sklearn.metrics import roc_curve, auc, roc_auc_score
from scipy import stats

# --- Конфигурация ---
# Пути к данным
DATA_DIR = Path("prepared_data")
DATA_FILE = DATA_DIR / "analysis_ready_data.parquet"
METADATA_FILE = DATA_DIR / "data_metadata.json"
OUTPUT_DIR = Path("analysis_results")

# Модели для анализа
MODELS = {
    'meld_only': {
        'name': 'MELD only',
        'formula': 'lab_meld',
        'description': 'Базовая модель только с MELD score'
    },
    'meld_lowamvi': {
        'name': 'MELD + LowAMVI',
        'formula': 'lab_meld + low_AMVI + age + sex',
        'description': 'MELD с добавлением LowAMVI, возраста и пола'
    },
    'bc_meld_va': {
        'name': 'BC-MELD-VA',
        'formula': 'lab_meld + low_AMVI + high_IMAC + high_VSR + age + sex',
        'description': 'Полная модель с всеми параметрами состава тела'
    }
}

# Временные точки для ROC анализа
TIME_POINTS = [3, 6, 12]  # месяцы

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

def load_data(logger):
    """Загрузка данных и метаданных"""
    logger.info("Загрузка данных...")
    
    # Загрузка данных
    df = pd.read_parquet(DATA_FILE)
    logger.info(f"Загружены данные формы: {df.shape}")
    
    # Загрузка метаданных
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    logger.info("Метаданные загружены")
    
    return df, metadata

def perform_cox_regression(df, model_config, logger):
    """Выполнение Cox регрессии"""
    logger.info(f"Выполнение Cox регрессии для модели {model_config['name']}...")
    
    cph = CoxPHFitter()
    cph.fit(
        df,
        duration_col='surv_time_months',
        event_col='surv_status',
        formula=model_config['formula']
    )
    
    # Сохранение результатов
    results = {
        'model_name': model_config['name'],
        'description': model_config['description'],
        'concordance_index': cph.concordance_index_,
        'hazard_ratios': cph.hazard_ratios_.to_dict(),
        'p_values': cph.summary['p'].to_dict(),
        'confidence_intervals': {
            'lower': cph.confidence_intervals_['coef lower 95%'].to_dict(),
            'upper': cph.confidence_intervals_['coef upper 95%'].to_dict()
        }
    }
    
    return results, cph

def perform_kaplan_meier(df, group_col, logger):
    """Выполнение Kaplan-Meier анализа"""
    logger.info(f"Выполнение Kaplan-Meier анализа для {group_col}...")
    
    kmf = KaplanMeierFitter()
    groups = df[group_col].unique()
    
    results = {}
    plt.figure(figsize=(10, 6))
    
    for group in groups:
        mask = df[group_col] == group
        kmf.fit(
            df[mask]['surv_time_months'],
            df[mask]['surv_status'],
            label=str(group)
        )
        kmf.plot()
        
        results[group] = {
            'median_survival': kmf.median_survival_time_,
            'mean_survival': kmf.mean_survival_time_,
            'survival_at_times': {
                str(t): kmf.survival_function_.loc[t].values[0]
                for t in TIME_POINTS
            }
        }
    
    plt.title(f'Kaplan-Meier кривые по {group_col}')
    plt.xlabel('Время (месяцы)')
    plt.ylabel('Вероятность выживания')
    plt.savefig(OUTPUT_DIR / f'km_curves_{group_col}.png')
    plt.close()
    
    return results

def perform_roc_analysis(df, model_config, time_point, logger):
    """Выполнение ROC анализа"""
    logger.info(f"Выполнение ROC анализа для {model_config['name']} на {time_point} месяцев...")
    
    # Подготовка данных
    mask = df['surv_time_months'] <= time_point
    y_true = df[mask]['surv_status']
    
    # Получение предсказаний
    cph = CoxPHFitter()
    cph.fit(
        df,
        duration_col='surv_time_months',
        event_col='surv_status',
        formula=model_config['formula']
    )
    predictions = cph.predict_partial_risk(df[mask])
    
    # ROC анализ
    fpr, tpr, _ = roc_curve(y_true, predictions)
    auc_score = roc_auc_score(y_true, predictions)
    
    # Построение графика
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f'AUC = {auc_score:.3f}')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC кривая для {model_config["name"]} на {time_point} месяцев')
    plt.legend()
    plt.savefig(OUTPUT_DIR / f'roc_curve_{model_config["name"]}_{time_point}m.png')
    plt.close()
    
    return {
        'auc': auc_score,
        'fpr': fpr.tolist(),
        'tpr': tpr.tolist()
    }

def perform_stratified_analysis(df, model_config, logger):
    """Выполнение стратифицированного анализа по MELD группам"""
    logger.info(f"Выполнение стратифицированного анализа для {model_config['name']}...")
    
    results = {}
    for meld_group in ['low', 'high']:
        mask = df['meld_group'] == meld_group
        if mask.sum() > 0:
            group_df = df[mask]
            
            # Cox регрессия
            cph = CoxPHFitter()
            cph.fit(
                group_df,
                duration_col='surv_time_months',
                event_col='surv_status',
                formula=model_config['formula']
            )
            
            results[meld_group] = {
                'concordance_index': cph.concordance_index_,
                'hazard_ratios': cph.hazard_ratios_.to_dict(),
                'p_values': cph.summary['p'].to_dict()
            }
    
    return results

def save_results(results, filename, logger):
    """Сохранение результатов анализа"""
    logger.info(f"Сохранение результатов в {filename}...")
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

def main():
    # Настройка логирования
    logger = setup_logging()
    logger.info("Начало анализа данных")
    
    # Создание выходной директории
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    try:
        # Загрузка данных
        df, metadata = load_data(logger)
        
        # Результаты анализа
        analysis_results = {
            'metadata': metadata,
            'models': {},
            'kaplan_meier': {},
            'roc_analysis': {},
            'stratified_analysis': {}
        }
        
        # Анализ для каждой модели
        for model_key, model_config in MODELS.items():
            logger.info(f"\nАнализ модели: {model_config['name']}")
            
            # Cox регрессия
            cox_results, _ = perform_cox_regression(df, model_config, logger)
            analysis_results['models'][model_key] = cox_results
            
            # ROC анализ для разных временных точек
            roc_results = {}
            for time_point in TIME_POINTS:
                roc_results[str(time_point)] = perform_roc_analysis(
                    df, model_config, time_point, logger
                )
            analysis_results['roc_analysis'][model_key] = roc_results
            
            # Стратифицированный анализ
            stratified_results = perform_stratified_analysis(df, model_config, logger)
            analysis_results['stratified_analysis'][model_key] = stratified_results
        
        # Kaplan-Meier анализ для разных группировок
        for group_col in ['meld_group', 'low_AMVI', 'high_IMAC', 'high_VSR']:
            if group_col in df.columns:
                km_results = perform_kaplan_meier(df, group_col, logger)
                analysis_results['kaplan_meier'][group_col] = km_results
        
        # Сохранение результатов
        save_results(
            analysis_results,
            OUTPUT_DIR / "analysis_results.json",
            logger
        )
        
        logger.info("\nАнализ завершен успешно")
        logger.info(f"Результаты сохранены в: {OUTPUT_DIR}")
        
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main() 