# -*- coding: utf-8 -*-
#
# Copyright 2017 Ricequant, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from rqalpha.interface import AbstractFrontendValidator

from rqalpha.utils.i18n import gettext as _


class IsTradingValidator(AbstractFrontendValidator):
    def __init__(self, env):
        self._env = env

    def can_submit_order(self, account, order):
        instrument = self._env.data_proxy.instruments(order.order_book_id)
        if instrument.listed_date > self._env.trading_dt:
            order.mark_rejected(_(u"Order Rejected: {order_book_id} is not listed!").format(
                order_book_id=order.order_book_id,
            ))
            return False

        if instrument.de_listed_date.date() < self._env.trading_dt.date():
            order.mark_rejected(_(u"Order Rejected: {order_book_id} has been delisted!").format(
                order_book_id=order.order_book_id,
            ))
            return False

        if self._env.data_proxy.is_suspended(order.order_book_id, self._env.trading_dt):
            order.mark_rejected(_('security {order_book_id} is suspended on {date}').format(
                order_book_id=order.order_book_id,
                date=self._env.trading_dt
            ))
            return False

        return True

    def can_cancel_order(self, account, order):
        return True
