# Управление конфигурацией проекта XizmatGo

## Элементы конфигурации (SCI)
| ID | Элемент | Расположение | Ответственный |
|---|---|---|---|
| SCI-01 | ТЗ, анализ, модель процесса (ПР-1) | docs/PR01_analiz_TZ_model.pdf | Камбарова Х. (PO) |
| SCI-02 | Бэклог продукта, план спринта (ПР-2) | docs/PR02_scrum_backlog.pdf | Камбарова Х. (PO) |
| SCI-03 | Архитектура и прототип (ПР-3) | docs/PR03_prototip.pdf | Рахимов Ж. (техлид) |
| SCI-04 | Команда, RACI (ПР-4) | docs/PR04_komanda.pdf, docs/PR04_tablitsy.xlsx | Камбарова Х. (PO) |
| SCI-05 | Спецификация требований SRS, UC (ПР-5) | docs/PR05_trebovaniya_UC.pdf | Камбарова Х. (PO) |
| SCI-06 | Модель проектирования, UML (ПР-6) | docs/PR06_proektirovanie_UML.pdf | Рахимов Ж. (техлид) |
| SCI-07 | UX: персоны, вайрфреймы (ПР-7) | docs/PR07_UI_UX.pdf, docs/PR07_vayrfreymy.drawio | Ахмедов Б. (UX) |
| SCI-08 | Паттерны проектирования (ПР-8) | docs/PR08_patterny.pdf, src/xizmatgo/matching.py | Рахимов Ж. (техлид) |
| SCI-09 | Требования к качеству, план SQA (ПР-9) | docs/PR09_kachestvo_SQA.pdf | Ким Д. (QA) |
| SCI-10 | Модель угроз, требования безопасности (ПР-10) | docs/PR10_bezopasnost.pdf | Рахимов Ж. (техлид) |
| SCI-11 | Тест-план, тест-кейсы (ПР-11) | docs/PR11_testirovanie.pdf, docs/PR11_potokovyi_graf.drawio | Ким Д. (QA) |
| SCI-12 | Исходный код компонентов | src/xizmatgo/ | Рахимов Ж., Юсупова М. |
| SCI-13 | Модульные тесты | tests/, pytest.ini | Ким Д. (QA) |
| SCI-14 | CI-конвейер | .github/workflows/ci.yml | Ким Д. (QA) |
| SCI-15 | Шаблоны CR и PR | .github/ISSUE_TEMPLATE/, .github/pull_request_template.md | Камбарова Х. (PO) |
| SCI-16 | Описание проекта, журнал изменений, правила | README.md, CHANGELOG.md, docs/CONFIGURATION.md, .gitignore | Камбарова Х. (PO) |

## Базовые линии
| Базовая линия | Тег | Состав | Момент фиксации |
|---|---|---|---|
| BL-1 «Требования и проект» | `bl-1-requirements` | SCI-01 … SCI-11 | после утверждения ТЗ, SRS и модели проектирования |
| BL-2 «Выпуск 1.0.0» | `v1.0.0` | SCI-01 … SCI-16 | после приёмки первого выпуска |

## Ветвление
- `main` — только выпущенные версии, каждый коммит отмечен тегом;
- `develop` — интеграционная ветка следующего выпуска;
- `feature/XG-<номер>-<кратко>` — одна задача бэклога, создаётся от `develop`, вливается через PR;
- `hotfix/XG-<номер>-<кратко>` — срочное исправление от `main`, вливается в `main` и `develop`.

## Коммиты (Conventional Commits)
`<тип>(<область>): <что сделано> [XG-<номер>]`, типы: feat, fix, test, docs, refactor, chore, ci.
