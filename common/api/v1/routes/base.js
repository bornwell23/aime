import express from 'express';
import { BaseController } from '../controllers/base.js';

const router = express.Router();
const controller = new BaseController();

router.get('/', controller.getAll);
router.get('/:id', controller.getById);
router.post('/', controller.create);
router.put('/:id', controller.update);
router.delete('/:id', controller.delete);

export default router;
