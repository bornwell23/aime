import express from 'express';
import { ExampleController } from '../../../controllers/example.controller.js';

const router = express.Router();
const controller = new ExampleController();

router.get('/', controller.getAll);
router.get('/:id', controller.getById);
router.post('/', controller.create);
router.put('/:id', controller.update);
router.delete('/:id', controller.delete);

export default router;
