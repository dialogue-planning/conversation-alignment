(define
    (domain medical_bot)
    (:requirements :strips)
    (:types )
    (:constants )
    (:predicates
        (know__have-symptoms)
        (have-symptoms)
        (know__symptoms)
        (know__over-week)
        (over-week)
        (know__covid-exposure)
        (covid-exposure)
        (know__exposure-period-over-5)
        (exposure-period-over-5)
        (know__positive-30)
        (positive-30)
        (know__positive-90)
        (positive-90)
        (know__need-reg-diag)
        (need-reg-diag)
        (know__need-covid-diag)
        (need-covid-diag)
        (ran-reg-diag)
        (ran-covid-diag)
        (no-covid-symptoms)
        (completed-diagnostics)
        (goal)
        (force-statement)
        (forcing__diagnose_regular_sickness)
    )
    (:action get_symptoms
        :parameters()
        :precondition
            (and
                (not (force-statement))
                (not (know__symptoms))
                (not (forcing__diagnose_regular_sickness))
                (have-symptoms)
            )
        :effect
            (labeled-oneof get_symptoms__get-symptoms
                (outcome share-covid
                    (and
                        (not (no-covid-symptoms))
                        (know__symptoms)
                    )
                )
                (outcome share-rash
                    (and
                        (know__symptoms)
                        (no-covid-symptoms)
                    )
                )
                (outcome share-teeth
                    (and
                        (know__symptoms)
                        (no-covid-symptoms)
                    )
                )
                (outcome fallback
                    (and
                        (force-statement)
                    )
                )
            )
    )
    (:action progress_no_symptoms_cases
        :parameters()
        :precondition
            (and
                (not (know__need-covid-diag))
                (not (have-symptoms))
                (know__covid-exposure)
                (not (forcing__diagnose_regular_sickness))
                (know__have-symptoms)
                (not (force-statement))
                (not (completed-diagnostics))
            )
        :effect
            (labeled-oneof progress_no_symptoms_cases__check-test
                (outcome no-exposure-no-symptoms
                    (and
                        (force-statement)
                        (completed-diagnostics)
                    )
                )
                (outcome proceed
                    (and
                        (know__need-covid-diag)
                        (need-covid-diag)
                        (know__need-reg-diag)
                        (force-statement)
                        (not (need-reg-diag))
                        (no-covid-symptoms)
                    )
                )
            )
    )
    (:action progress_symptoms_cases
        :parameters()
        :precondition
            (and
                (not (know__need-covid-diag))
                (have-symptoms)
                (know__covid-exposure)
                (know__symptoms)
                (not (forcing__diagnose_regular_sickness))
                (not (force-statement))
                (not (know__need-reg-diag))
            )
        :effect
            (labeled-oneof progress_symptoms_cases__check-test
                (outcome covid
                    (and
                        (know__need-covid-diag)
                        (need-covid-diag)
                        (not (need-reg-diag))
                        (know__need-reg-diag)
                    )
                )
                (outcome rash-covid
                    (and
                        (know__need-covid-diag)
                        (forcing__diagnose_regular_sickness)
                        (need-covid-diag)
                        (know__need-reg-diag)
                        (need-reg-diag)
                    )
                )
                (outcome teeth-covid
                    (and
                        (know__need-covid-diag)
                        (forcing__diagnose_regular_sickness)
                        (need-covid-diag)
                        (know__need-reg-diag)
                        (need-reg-diag)
                    )
                )
                (outcome rash-no-covid
                    (and
                        (know__need-covid-diag)
                        (need-reg-diag)
                        (know__need-reg-diag)
                        (not (need-covid-diag))
                    )
                )
                (outcome teeth-no-covid
                    (and
                        (know__need-covid-diag)
                        (need-reg-diag)
                        (know__need-reg-diag)
                        (not (need-covid-diag))
                    )
                )
            )
    )
    (:action diagnose_regular_sickness
        :parameters()
        :precondition
            (and
                (know__over-week)
                (need-reg-diag)
                (not (force-statement))
                (not (ran-reg-diag))
            )
        :effect
            (labeled-oneof diagnose_regular_sickness__check-test
                (outcome rash-under
                    (and
                        (ran-reg-diag)
                        (not (forcing__diagnose_regular_sickness))
                        (force-statement)
                    )
                )
                (outcome rash-over
                    (and
                        (ran-reg-diag)
                        (not (forcing__diagnose_regular_sickness))
                        (force-statement)
                    )
                )
                (outcome teeth
                    (and
                        (ran-reg-diag)
                        (not (forcing__diagnose_regular_sickness))
                        (force-statement)
                    )
                )
            )
    )
    (:action determine_covid_test
        :parameters()
        :precondition
            (and
                (know__positive-30)
                (know__covid-exposure)
                (not (ran-covid-diag))
                (need-covid-diag)
                (know__symptoms)
                (know__positive-90)
                (know__exposure-period-over-5)
                (not (forcing__diagnose_regular_sickness))
                (not (force-statement))
            )
        :effect
            (labeled-oneof determine_covid_test__check-test
                (outcome have-no-symptoms-30
                    (and
                        (force-statement)
                        (ran-covid-diag)
                    )
                )
                (outcome have-symptoms-30
                    (and
                        (force-statement)
                        (ran-covid-diag)
                    )
                )
                (outcome have-symptoms-no-90
                    (and
                        (force-statement)
                        (ran-covid-diag)
                    )
                )
                (outcome have-symptoms-90
                    (and
                        (force-statement)
                        (ran-covid-diag)
                    )
                )
                (outcome have-no-symptoms-90
                    (and
                        (force-statement)
                        (ran-covid-diag)
                    )
                )
                (outcome no-symptom-exposed-been-5
                    (and
                        (force-statement)
                        (ran-covid-diag)
                    )
                )
                (outcome no-symptom-exposed-less-5
                    (and
                        (force-statement)
                        (ran-covid-diag)
                    )
                )
            )
    )
    (:action got-both-diags
        :parameters()
        :precondition
            (and
                (know__need-covid-diag)
                (need-covid-diag)
                (ran-reg-diag)
                (ran-covid-diag)
                (not (forcing__diagnose_regular_sickness))
                (not (force-statement))
                (know__need-reg-diag)
                (need-reg-diag)
                (not (completed-diagnostics))
            )
        :effect
            (labeled-oneof got-both-diags__check-test
                (outcome complete
                    (and
                        (completed-diagnostics)
                    )
                )
            )
    )
    (:action got-covid-diag
        :parameters()
        :precondition
            (and
                (know__need-covid-diag)
                (need-covid-diag)
                (not (forcing__diagnose_regular_sickness))
                (ran-covid-diag)
                (not (force-statement))
                (know__need-reg-diag)
                (not (need-reg-diag))
                (not (completed-diagnostics))
            )
        :effect
            (labeled-oneof got-covid-diag__check-test
                (outcome complete
                    (and
                        (completed-diagnostics)
                    )
                )
            )
    )
    (:action got-reg-diag
        :parameters()
        :precondition
            (and
                (know__need-covid-diag)
                (ran-reg-diag)
                (not (forcing__diagnose_regular_sickness))
                (not (need-covid-diag))
                (not (force-statement))
                (know__need-reg-diag)
                (need-reg-diag)
                (not (completed-diagnostics))
            )
        :effect
            (labeled-oneof got-reg-diag__check-test
                (outcome complete
                    (and
                        (completed-diagnostics)
                    )
                )
            )
    )
    (:action complete
        :parameters()
        :precondition
            (and
                (not (force-statement))
                (completed-diagnostics)
                (not (forcing__diagnose_regular_sickness))
            )
        :effect
            (labeled-oneof complete__finish
                (outcome finish
                    (and
                        (goal)
                    )
                )
            )
    )
    (:action dialogue_statement
        :parameters()
        :precondition
            (and
                (force-statement)
            )
        :effect
            (labeled-oneof dialogue_statement__reset
                (outcome lock
                    (and
                        (not (force-statement))
                    )
                )
            )
    )
    (:action slot-fill__get_have_symptoms
        :parameters()
        :precondition
            (and
                (not (know__have-symptoms))
                (not (force-statement))
                (not (forcing__diagnose_regular_sickness))
            )
        :effect
            (labeled-oneof slot-fill__get_have_symptoms__get-response
                (outcome confirm_outcome
                    (and
                        (force-statement)
                        (know__have-symptoms)
                        (have-symptoms)
                    )
                )
                (outcome deny_outcome
                    (and
                        (know__symptoms)
                        (not (have-symptoms))
                        (know__have-symptoms)
                    )
                )
                (outcome fallback
                    (and
                        (force-statement)
                    )
                )
            )
    )
    (:action slot-fill__get_sickness_period
        :parameters()
        :precondition
            (and
                (not (know__over-week))
                (not (force-statement))
                (not (forcing__diagnose_regular_sickness))
                (have-symptoms)
            )
        :effect
            (labeled-oneof slot-fill__get_sickness_period__get-response
                (outcome confirm_outcome
                    (and
                        (know__over-week)
                        (over-week)
                    )
                )
                (outcome deny_outcome
                    (and
                        (know__over-week)
                        (not (over-week))
                    )
                )
                (outcome fallback
                    (and
                        (force-statement)
                    )
                )
            )
    )
    (:action slot-fill__get_covid_exposure
        :parameters()
        :precondition
            (and
                (not (know__covid-exposure))
                (not (force-statement))
                (not (forcing__diagnose_regular_sickness))
            )
        :effect
            (labeled-oneof slot-fill__get_covid_exposure__get-response
                (outcome confirm_outcome
                    (and
                        (know__covid-exposure)
                        (covid-exposure)
                    )
                )
                (outcome deny_outcome
                    (and
                        (know__covid-exposure)
                        (not (covid-exposure))
                    )
                )
                (outcome fallback
                    (and
                        (force-statement)
                    )
                )
            )
    )
    (:action slot-fill__get_exposure_period
        :parameters()
        :precondition
            (and
                (know__covid-exposure)
                (need-covid-diag)
                (not (forcing__diagnose_regular_sickness))
                (not (force-statement))
                (not (know__exposure-period-over-5))
            )
        :effect
            (labeled-oneof slot-fill__get_exposure_period__get-response
                (outcome confirm_outcome
                    (and
                        (know__exposure-period-over-5)
                        (exposure-period-over-5)
                    )
                )
                (outcome deny_outcome
                    (and
                        (know__exposure-period-over-5)
                        (not (exposure-period-over-5))
                    )
                )
                (outcome fallback
                    (and
                        (force-statement)
                    )
                )
            )
    )
    (:action slot-fill__get_positive_30
        :parameters()
        :precondition
            (and
                (need-covid-diag)
                (not (know__positive-30))
                (not (forcing__diagnose_regular_sickness))
                (not (force-statement))
            )
        :effect
            (labeled-oneof slot-fill__get_positive_30__get-response
                (outcome confirm_outcome
                    (and
                        (positive-30)
                        (know__positive-90)
                        (know__positive-30)
                        (positive-90)
                    )
                )
                (outcome deny_outcome
                    (and
                        (know__positive-30)
                        (not (positive-30))
                    )
                )
                (outcome fallback
                    (and
                        (force-statement)
                    )
                )
            )
    )
    (:action slot-fill__get_positive_90
        :parameters()
        :precondition
            (and
                (know__positive-30)
                (not (positive-30))
                (not (forcing__diagnose_regular_sickness))
                (not (force-statement))
                (not (know__positive-90))
            )
        :effect
            (labeled-oneof slot-fill__get_positive_90__get-response
                (outcome confirm_outcome
                    (and
                        (know__positive-90)
                        (positive-90)
                    )
                )
                (outcome deny_outcome
                    (and
                        (not (positive-90))
                        (know__positive-90)
                    )
                )
                (outcome fallback
                    (and
                        (force-statement)
                    )
                )
            )
    )
)