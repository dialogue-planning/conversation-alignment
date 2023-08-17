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
                        (not (task-value-request_money))
                        (task-value-transfer_funds_between_accounts)
                        (not (task-value-create_account))
                        (know__task)
                        (not (task-value-e-transfer))
                        (not (task-value-pay_bills))
                    )
                )
                (outcome dont-want
                    (and
                        (tried-transfer)
                        (force-statement)
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
                (task-value-transfer_funds_between_accounts)
                (not (force-statement))
            )
        :effect
            (labeled-oneof get-transfer-options__get-options
                (outcome get-valid-options
                    (and
                        (know__funds)
                        (know__account1)
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
                (task-value-transfer_funds_between_accounts)
                (know__account2)
                (know__funds)
                (not (force-statement))
            )
        :effect
            (labeled-oneof confirm-transfer__transfer
                (outcome complete
                    (and
                        (not (task-value-transfer_funds_between_accounts))
                        (not (know__task))
                        (not (task-value-request_money))
                        (not (task-value-create_account))
                        (not (know__account2))
                        (tried-transfer)
                        (not (know__account1))
                        (not (task-value-e-transfer))
                        (not (task-value-pay_bills))
                        (not (know__funds))
                    )
                )
            )
    )
    (:action offer-e-transfer
        :parameters()
        :precondition
            (and
                (not (know__task))
                (not (tried-e-transfer))
                (not (force-statement))
            )
        :effect
            (labeled-oneof offer-e-transfer__start-task
                (outcome want-transfer
                    (and
                        (not (task-value-transfer_funds_between_accounts))
                        (task-value-e-transfer)
                        (not (task-value-request_money))
                        (not (task-value-create_account))
                        (know__task)
                        (not (task-value-pay_bills))
                    )
                )
                (outcome dont-want
                    (and
                        (tried-e-transfer)
                        (force-statement)
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
                        (select-account)
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
    (:action confirm-e-transfer
        :parameters()
        :precondition
            (and
                (know__account1)
                (know__contact)
                (task-value-e-transfer)
                (know__funds)
                (not (force-statement))
            )
        :effect
            (labeled-oneof confirm-e-transfer__reset
                (outcome complete
                    (and
                        (not (task-value-transfer_funds_between_accounts))
                        (not (know__task))
                        (not (task-value-request_money))
                        (not (know__contact))
                        (not (task-value-create_account))
                        (not (know__account1))
                        (tried-e-transfer)
                        (not (task-value-e-transfer))
                        (not (task-value-pay_bills))
                        (not (know__funds))
                    )
                )
            )
    )
    (:action offer-request
        :parameters()
        :precondition
            (and
                (not (tried-request-money))
                (not (know__task))
                (not (force-statement))
            )
        :effect
            (labeled-oneof offer-request__start-task
                (outcome want-transfer
                    (and
                        (not (task-value-transfer_funds_between_accounts))
                        (task-value-request_money)
                        (not (task-value-create_account))
                        (know__task)
                        (not (task-value-e-transfer))
                        (not (task-value-pay_bills))
                    )
                )
                (outcome dont-want
                    (and
                        (tried-request-money)
                        (force-statement)
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
                (know__funds)
                (task-value-request_money)
                (know__contact)
                (not (force-statement))
            )
        :effect
            (labeled-oneof confirm-request__reset
                (outcome complete
                    (and
                        (not (task-value-transfer_funds_between_accounts))
                        (not (know__task))
                        (not (task-value-request_money))
                        (tried-request-money)
                        (not (know__contact))
                        (not (task-value-create_account))
                        (not (task-value-e-transfer))
                        (not (task-value-pay_bills))
                        (not (know__funds))
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
                        (not (task-value-request_money))
                        (task-value-pay_bills)
                        (not (task-value-create_account))
                        (know__task)
                        (not (task-value-e-transfer))
                    )
                )
                (outcome dont-want
                    (and
                        (tried-pay-bills)
                        (force-statement)
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
                        (not (know__bill))
                        (not (know__task))
                        (not (task-value-transfer_funds_between_accounts))
                        (tried-pay-bills)
                        (not (task-value-request_money))
                        (not (task-value-create_account))
                        (not (know__account1))
                        (not (task-value-e-transfer))
                        (not (task-value-pay_bills))
                    )
                )
            )
    )
    (:action offer-new
        :parameters()
        :precondition
            (and
                (not (know__task))
                (not (tried-create))
                (not (force-statement))
            )
        :effect
            (labeled-oneof offer-new__start-task
                (outcome want-create
                    (and
                        (not (task-value-transfer_funds_between_accounts))
                        (task-value-create_account)
                        (not (task-value-request_money))
                        (know__task)
                        (not (task-value-e-transfer))
                        (not (task-value-pay_bills))
                    )
                )
                (outcome dont-want
                    (and
                        (tried-create)
                        (force-statement)
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
                (task-value-create_account)
                (know__account1)
                (not (force-statement))
                (know__account2)
            )
        :effect
            (labeled-oneof confirm-create__reset
                (outcome complete
                    (and
                        (not (task-value-transfer_funds_between_accounts))
                        (not (know__task))
                        (tried-create)
                        (not (task-value-request_money))
                        (not (task-value-create_account))
                        (not (know__account2))
                        (not (know__account1))
                        (not (task-value-e-transfer))
                        (not (task-value-pay_bills))
                    )
                )
            )
    )
    (:action complete
        :parameters()
        :precondition
            (and
                (tried-create)
                (tried-pay-bills)
                (tried-transfer)
                (tried-e-transfer)
                (not (force-statement))
                (tried-request-money)
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
                (select-account)
                (not (know__account1))
                (not (force-statement))
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
                        (select-account)
                        (know__bill)
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
                (task-value-create_account)
                (not (know__account2))
                (not (force-statement))
            )
        :effect
            (labeled-oneof slot-fill__get-create__validate-slot-fill
                (outcome account2_found
                    (and
                        (select-account)
                        (force-statement)
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
)