(define
    (domain bank-bot)
    (:requirements :strips)
    (:types )
    (:constants )
    (:predicates
        (select-account)
        (know__task)
        (tried-transfer)
        (tried-e-transfer)
        (tried-request-money)
        (tried-pay-bills)
        (tried-create)
        (know__account1)
        (know__account2)
        (know__funds)
        (know__contact)
        (know__bill)
        (know__goal)
        (goal)
        (force-statement)
        (task-value-transfer_funds_between_accounts)
        (task-value-e-transfer)
        (task-value-request_money)
        (task-value-pay_bills)
        (task-value-create_account)
    )
    (:action offer-transfer
        :parameters()
        :precondition
            (and
                (not (tried-transfer))
                (not (know__task))
                (not (force-statement))
            )
        :effect
            (labeled-oneof offer-transfer__start-task
                (outcome want-transfer
                    (and
                        (not (task-value-pay_bills))
                        (not (task-value-request_money))
                        (task-value-transfer_funds_between_accounts)
                        (not (task-value-e-transfer))
                        (not (task-value-create_account))
                        (know__task)
                    )
                )
                (outcome dont-want
                    (and
                        (force-statement)
                        (tried-transfer)
                    )
                )
                (outcome fallback
                    (and
                        (force-statement)
                    )
                )
            )
    )
    (:action get-transfer-options
        :parameters()
        :precondition
            (and
                (not (force-statement))
                (task-value-transfer_funds_between_accounts)
            )
        :effect
            (labeled-oneof get-transfer-options__get-options
                (outcome get-valid-options
                    (and
                        (know__account1)
                        (know__funds)
                        (know__account2)
                    )
                )
                (outcome fallback
                    (and
                        (force-statement)
                    )
                )
            )
    )
    (:action confirm-transfer
        :parameters()
        :precondition
            (and
                (know__account1)
                (know__funds)
                (know__account2)
                (task-value-transfer_funds_between_accounts)
                (not (force-statement))
            )
        :effect
            (labeled-oneof confirm-transfer__transfer
                (outcome complete
                    (and
                        (not (task-value-transfer_funds_between_accounts))
                        (not (task-value-pay_bills))
                        (not (know__funds))
                        (not (task-value-request_money))
                        (tried-transfer)
                        (not (know__account2))
                        (not (task-value-e-transfer))
                        (not (task-value-create_account))
                        (not (know__account1))
                        (not (know__task))
                    )
                )
            )
    )
    (:action offer-e-transfer
        :parameters()
        :precondition
            (and
                (not (tried-e-transfer))
                (not (know__task))
                (not (force-statement))
            )
        :effect
            (labeled-oneof offer-e-transfer__start-task
                (outcome want-transfer
                    (and
                        (not (task-value-transfer_funds_between_accounts))
                        (not (task-value-pay_bills))
                        (not (task-value-request_money))
                        (not (task-value-create_account))
                        (know__task)
                        (task-value-e-transfer)
                    )
                )
                (outcome dont-want
                    (and
                        (force-statement)
                        (tried-e-transfer)
                    )
                )
                (outcome fallback
                    (and
                        (force-statement)
                    )
                )
            )
    )
    (:action get-e-transfer-options
        :parameters()
        :precondition
            (and
                (not (force-statement))
                (task-value-e-transfer)
            )
        :effect
            (labeled-oneof get-e-transfer-options__get-options
                (outcome get-valid-e-transfer
                    (and
                        (know__funds)
                        (know__contact)
                        (select-account)
                    )
                )
                (outcome fallback
                    (and
                        (force-statement)
                    )
                )
            )
    )
    (:action confirm-e-transfer
        :parameters()
        :precondition
            (and
                (know__account1)
                (know__funds)
                (know__contact)
                (not (force-statement))
                (task-value-e-transfer)
            )
        :effect
            (labeled-oneof confirm-e-transfer__reset
                (outcome complete
                    (and
                        (not (task-value-transfer_funds_between_accounts))
                        (not (task-value-pay_bills))
                        (tried-e-transfer)
                        (not (know__funds))
                        (not (task-value-request_money))
                        (not (task-value-e-transfer))
                        (not (know__contact))
                        (not (task-value-create_account))
                        (not (know__account1))
                        (not (know__task))
                    )
                )
            )
    )
    (:action offer-request
        :parameters()
        :precondition
            (and
                (not (know__task))
                (not (tried-request-money))
                (not (force-statement))
            )
        :effect
            (labeled-oneof offer-request__start-task
                (outcome want-transfer
                    (and
                        (not (task-value-transfer_funds_between_accounts))
                        (not (task-value-pay_bills))
                        (not (task-value-e-transfer))
                        (not (task-value-create_account))
                        (task-value-request_money)
                        (know__task)
                    )
                )
                (outcome dont-want
                    (and
                        (force-statement)
                        (tried-request-money)
                    )
                )
                (outcome fallback
                    (and
                        (force-statement)
                    )
                )
            )
    )
    (:action get-request-options
        :parameters()
        :precondition
            (and
                (task-value-request_money)
                (not (force-statement))
            )
        :effect
            (labeled-oneof get-request-options__get-options
                (outcome get-valid-request
                    (and
                        (know__funds)
                        (know__contact)
                    )
                )
                (outcome fallback
                    (and
                        (force-statement)
                    )
                )
            )
    )
    (:action confirm-request
        :parameters()
        :precondition
            (and
                (task-value-request_money)
                (not (force-statement))
                (know__funds)
                (know__contact)
            )
        :effect
            (labeled-oneof confirm-request__reset
                (outcome complete
                    (and
                        (not (task-value-transfer_funds_between_accounts))
                        (not (task-value-pay_bills))
                        (not (know__funds))
                        (not (task-value-request_money))
                        (tried-request-money)
                        (not (task-value-e-transfer))
                        (not (know__contact))
                        (not (task-value-create_account))
                        (not (know__task))
                    )
                )
            )
    )
    (:action offer-pay
        :parameters()
        :precondition
            (and
                (not (know__task))
                (not (tried-pay-bills))
                (not (force-statement))
            )
        :effect
            (labeled-oneof offer-pay__start-task
                (outcome want-pay
                    (and
                        (not (task-value-transfer_funds_between_accounts))
                        (task-value-pay_bills)
                        (not (task-value-request_money))
                        (not (task-value-e-transfer))
                        (not (task-value-create_account))
                        (know__task)
                    )
                )
                (outcome dont-want
                    (and
                        (force-statement)
                        (tried-pay-bills)
                    )
                )
                (outcome fallback
                    (and
                        (force-statement)
                    )
                )
            )
    )
    (:action confirm-bill-payment
        :parameters()
        :precondition
            (and
                (know__account1)
                (know__bill)
                (task-value-pay_bills)
                (not (force-statement))
            )
        :effect
            (labeled-oneof confirm-bill-payment__reset
                (outcome complete
                    (and
                        (not (task-value-transfer_funds_between_accounts))
                        (not (task-value-pay_bills))
                        (not (task-value-request_money))
                        (not (know__bill))
                        (tried-pay-bills)
                        (not (task-value-e-transfer))
                        (not (task-value-create_account))
                        (not (know__account1))
                        (not (know__task))
                    )
                )
            )
    )
    (:action offer-new
        :parameters()
        :precondition
            (and
                (not (tried-create))
                (not (know__task))
                (not (force-statement))
            )
        :effect
            (labeled-oneof offer-new__start-task
                (outcome want-create
                    (and
                        (not (task-value-transfer_funds_between_accounts))
                        (not (task-value-pay_bills))
                        (not (task-value-request_money))
                        (task-value-create_account)
                        (not (task-value-e-transfer))
                        (know__task)
                    )
                )
                (outcome dont-want
                    (and
                        (force-statement)
                        (tried-create)
                    )
                )
                (outcome fallback
                    (and
                        (force-statement)
                    )
                )
            )
    )
    (:action confirm-create
        :parameters()
        :precondition
            (and
                (know__account1)
                (know__account2)
                (task-value-create_account)
                (not (force-statement))
            )
        :effect
            (labeled-oneof confirm-create__reset
                (outcome complete
                    (and
                        (not (task-value-transfer_funds_between_accounts))
                        (not (task-value-pay_bills))
                        (not (task-value-request_money))
                        (not (know__account2))
                        (not (task-value-e-transfer))
                        (tried-create)
                        (not (task-value-create_account))
                        (not (know__account1))
                        (not (know__task))
                    )
                )
            )
    )
    (:action complete
        :parameters()
        :precondition
            (and
                (tried-e-transfer)
                (tried-transfer)
                (tried-request-money)
                (tried-pay-bills)
                (not (force-statement))
                (tried-create)
            )
        :effect
            (labeled-oneof complete__finish
                (outcome done
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
    (:action slot-fill__select-account
        :parameters()
        :precondition
            (and
                (not (force-statement))
                (select-account)
                (not (know__account1))
            )
        :effect
            (labeled-oneof slot-fill__select-account__validate-slot-fill
                (outcome account1_found
                    (and
                        (know__account1)
                        (not (select-account))
                    )
                )
                (outcome fallback
                    (and
                        (force-statement)
                    )
                )
            )
    )
    (:action slot-fill__get-payment
        :parameters()
        :precondition
            (and
                (not (know__bill))
                (task-value-pay_bills)
                (not (force-statement))
            )
        :effect
            (labeled-oneof slot-fill__get-payment__validate-slot-fill
                (outcome bill_found
                    (and
                        (know__bill)
                        (select-account)
                    )
                )
                (outcome fallback
                    (and
                        (force-statement)
                    )
                )
            )
    )
    (:action slot-fill__get-create
        :parameters()
        :precondition
            (and
                (not (know__account2))
                (task-value-create_account)
                (not (force-statement))
            )
        :effect
            (labeled-oneof slot-fill__get-create__validate-slot-fill
                (outcome account2_found
                    (and
                        (force-statement)
                        (know__account2)
                        (select-account)
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